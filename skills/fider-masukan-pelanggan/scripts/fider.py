#!/usr/bin/env python3
"""fider-masukan-pelanggan (Komunitech) - kelola papan masukan Fider milik pengguna sendiri.

Fider = papan masukan & voting fitur open-source (AGPL-3.0) yang dipasang di komputer/server milik
pengguna. Script ini memanggil REST API resmi Fider (/api/v1/..., header 'Authorization: Bearer <kunci>').
Python standar saja. Kunci API TIDAK PERNAH dicetak. Semua perintah yang MENULIS ke Fider hanya
menampilkan pratinjau, kecuali ditambah --ya (setelah pemilik setuju).

Perintah baca:   cek | daftar | cari | lihat | tag-daftar | ringkasan-mingguan | draf-balasan
Perintah tulis:  impor | tag | gabung | status | komentar | tag-buat   (semuanya butuh --ya)
Pengaturan:      simpan-kunci | simpan-alamat

Windows: pakai `python` atau `py` sebagai ganti `python3`. Tambah --json untuk hasil terstruktur.
"""
import argparse
import datetime as dt
import difflib
import getpass
import json
import os
import re
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSI = "1.0.0"
FOLDER_RAHASIA = os.path.join(os.path.expanduser("~"), ".komunitech")
KUNCI_DEFAULT = os.path.join(FOLDER_RAHASIA, "fider-kunci.txt")
ALAMAT_DEFAULT_FILE = os.path.join(FOLDER_RAHASIA, "fider-alamat.txt")
ALAMAT_BAWAAN = "http://localhost:3000"

STATUS_SAH = ("open", "planned", "started", "completed", "declined")
NAMA_STATUS = {
    "open": "Terbuka", "planned": "Direncanakan", "started": "Sedang dikerjakan",
    "completed": "Selesai", "declined": "Ditolak", "duplicate": "Duplikat",
}
ALIAS_STATUS = {
    "terbuka": "open", "baru": "open", "open": "open",
    "rencana": "planned", "direncanakan": "planned", "planned": "planned",
    "dikerjakan": "started", "mulai": "started", "started": "started",
    "selesai": "completed", "completed": "completed", "beres": "completed",
    "tolak": "declined", "ditolak": "declined", "declined": "declined",
}
BATAS_JUDUL = 100
BATAS_IMPOR = 50

# Kode keluar
K_OK, K_INPUT, K_KUNCI, K_JARINGAN, K_SERVER, K_FILE, K_IZIN = 0, 2, 3, 4, 5, 6, 7


class Gagal(Exception):
    def __init__(self, pesan, kode=K_SERVER):
        super().__init__(pesan)
        self.kode = kode


# ---------------------------------------------------------------- rahasia & alamat
def _cek_izin_file(path):
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
    os.makedirs(folder, mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(isi + "\n")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def _baca_file(path, sumber):
    try:
        _cek_izin_file(path)
        with open(path, encoding="utf-8") as f:
            teks = f.read().strip()
    except OSError as e:
        raise Gagal(f"Tidak bisa membaca {sumber} ({path}): {e.strerror}", K_KUNCI)
    if not teks:
        raise Gagal(f"{sumber} ({path}) kosong.", K_KUNCI)
    return teks


def ambil_kunci(args):
    """Urutan: --kunci-file, ENV FIDER_API_KEY, ENV FIDER_API_KEY_FILE, file default."""
    if args.kunci_file:
        return _baca_file(os.path.expanduser(args.kunci_file), "file kunci")
    if os.environ.get("FIDER_API_KEY", "").strip():
        return os.environ["FIDER_API_KEY"].strip()
    if os.environ.get("FIDER_API_KEY_FILE"):
        return _baca_file(os.path.expanduser(os.environ["FIDER_API_KEY_FILE"]), "FIDER_API_KEY_FILE")
    if os.path.isfile(KUNCI_DEFAULT):
        return _baca_file(KUNCI_DEFAULT, "file kunci")
    raise Gagal("Kunci API Fider belum ada. Jalankan SENDIRI: python3 scripts/fider.py simpan-kunci "
                "(kunci dibuat di Fider: menu profil > Settings > API Key).", K_KUNCI)


def samarkan(teks, kunci):
    """Hapus kunci dari teks apa pun yang akan dicetak (pertahanan berlapis)."""
    if kunci and kunci in teks:
        teks = teks.replace(kunci, "***")
    return teks


def alamat_awal(args):
    if args.url:
        return args.url.strip().rstrip("/"), True
    if os.environ.get("FIDER_URL", "").strip():
        return os.environ["FIDER_URL"].strip().rstrip("/"), True
    if os.path.isfile(ALAMAT_DEFAULT_FILE):
        return _baca_file(ALAMAT_DEFAULT_FILE, "file alamat").rstrip("/"), True
    return ALAMAT_BAWAAN, False


def host_lokal(host):
    if host in ("localhost", "127.0.0.1", "::1", "[::1]") or host.endswith(".local"):
        return True
    return bool(re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)", host))


def periksa_url(url):
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise Gagal(f"Alamat Fider tidak valid: {url!r} (contoh: http://localhost:3000 atau https://saran.tokosaya.id)", K_INPUT)
    if p.scheme == "http" and not host_lokal(p.hostname):
        raise Gagal("Alamat Fider di internet wajib HTTPS (kunci API tidak boleh lewat HTTP polos).", K_INPUT)
    if p.username or p.password:
        raise Gagal("Alamat Fider tidak boleh memuat sandi di dalamnya.", K_INPUT)


def simpan_kunci(args):
    path = os.path.abspath(os.path.expanduser(args.kunci_file)) if args.kunci_file else KUNCI_DEFAULT
    if os.path.exists(path) and not args.ya:
        raise Gagal(f"File kunci sudah ada: {path}\nUntuk mengganti, ulangi dengan --ya.", K_FILE)
    sys.stderr.write(f"Kunci akan disimpan di: {path}\n")
    kunci = getpass.getpass("Tempel kunci API Fider (tidak terlihat), lalu Enter: ").strip()
    if not kunci:
        raise Gagal("Kunci kosong, tidak disimpan.", K_INPUT)
    if re.search(r"\s", kunci):
        raise Gagal("Kunci berisi spasi/baris baru - kemungkinan tersalin rusak. Salin ulang.", K_INPUT)
    _tulis_rahasia(path, kunci)
    print(f"Kunci tersimpan di {path} (izin 600).")
    return K_OK


def simpan_alamat(args):
    if not args.alamat:
        raise Gagal("Tulis alamatnya: simpan-alamat https://saran.tokosaya.id", K_INPUT)
    url = args.alamat.strip().rstrip("/")
    periksa_url(url)
    _tulis_rahasia(ALAMAT_DEFAULT_FILE, url)
    print(f"Alamat tersimpan: {url}")
    return K_OK


# ---------------------------------------------------------------- klien HTTP
class _TanpaRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


class Klien:
    def __init__(self, url, kunci, timeout=20):
        self.url, self.kunci, self.timeout = url, kunci, timeout
        self.opener = urllib.request.build_opener(_TanpaRedirect)

    def minta(self, metode, path, badan=None, query=None):
        alamat = self.url + path
        if query:
            alamat += "?" + urllib.parse.urlencode(query, doseq=True)
        data = None if badan is None else json.dumps(badan).encode("utf-8")
        req = urllib.request.Request(alamat, data=data, method=metode)
        req.add_header("Authorization", "Bearer " + self.kunci)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "komunitech-fider-skill/" + VERSI)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with self.opener.open(req, timeout=self.timeout) as r:
                mentah = r.read()
        except urllib.error.HTTPError as e:
            self._galat_http(e, path)
        except urllib.error.URLError as e:
            raise Gagal(samarkan(f"Fider tidak terjangkau di {self.url} ({e.reason}). Pastikan Fider menyala "
                                 "(docker compose ps) dan alamatnya benar.", self.kunci), K_JARINGAN)
        except (TimeoutError, OSError) as e:
            raise Gagal(f"Waktu habis/jaringan putus saat menghubungi Fider: {e}", K_JARINGAN)
        if not mentah:
            return {}
        try:
            return json.loads(mentah.decode("utf-8"))
        except ValueError:
            raise Gagal("Jawaban Fider bukan JSON (mungkin alamat salah atau ada proxy di depannya).", K_SERVER)

    def _galat_http(self, e, path):
        isi = ""
        try:
            isi = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        pesan = ""
        try:
            errs = json.loads(isi).get("errors", [])
            pesan = "; ".join(x.get("message", "") for x in errs if x.get("message"))
        except ValueError:
            pass
        pesan = samarkan(pesan, self.kunci)
        if e.code in (301, 302, 303, 307, 308):
            raise Gagal("Fider mengalihkan (redirect) permintaan; ditolak demi keamanan kunci. "
                        "Periksa alamat (mungkin harus https://).", K_JARINGAN)
        if e.code == 400 and "API Key" in pesan:
            raise Gagal("Kunci API ditolak Fider (salah/sudah diganti). Buat kunci baru di Fider "
                        "(Settings > API Key) lalu jalankan simpan-kunci --ya.", K_KUNCI)
        if e.code in (401, 403):
            raise Gagal("Akses ditolak. Akun pemilik kunci harus berperan Collaborator/Administrator "
                        "(beberapa aksi, mis. tag baru, hanya untuk Administrator).", K_IZIN)
        if e.code == 404:
            raise Gagal(f"Tidak ditemukan ({path}). Nomor pos/tag salah?", K_INPUT)
        if e.code == 429:
            raise Gagal("Fider membatasi kecepatan permintaan (429). Tunggu semenit lalu ulangi.", K_SERVER)
        raise Gagal(f"Fider menjawab galat {e.code}" + (f": {pesan}" if pesan else "."), K_SERVER)


# ---------------------------------------------------------------- utilitas teks
def rapikan(teks):
    return re.sub(r"[ \t]+", " ", (teks or "").strip())


RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")
RE_HP = re.compile(r"(?<![\w])(?:\+?62|0)[\s.-]?8\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{2,5}(?!\d)")


def samarkan_pribadi(teks):
    """Papan Fider biasanya publik: sembunyikan nomor HP & email dari catatan WA sebelum ditulis."""
    n = 0

    def ganti(pesan):
        def f(_):
            nonlocal n
            n += 1
            return pesan
        return f
    teks = RE_EMAIL.sub(ganti("[email disembunyikan]"), teks)
    teks = RE_HP.sub(ganti("[nomor disembunyikan]"), teks)
    return teks, n


def potong(teks, batas):
    teks = rapikan(teks)
    if len(teks) <= batas:
        return teks
    return teks[: batas - 1].rstrip() + "…"


def normal(t):
    return re.sub(r"[^a-z0-9 ]+", " ", (t or "").lower()).split()


STOP = {"yang", "dan", "di", "ke", "untuk", "dengan", "ada", "tolong", "dong", "ya", "nih", "the", "a", "saya", "kami", "bisa", "mau", "minta"}


def kemiripan(a, b):
    ta, tb = [w for w in normal(a) if w not in STOP], [w for w in normal(b) if w not in STOP]
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    jaccard = len(sa & sb) / len(sa | sb)
    urut = difflib.SequenceMatcher(None, " ".join(ta), " ".join(tb)).ratio()
    return max(jaccard, urut * 0.9)


def angka(n):
    return f"{int(n):,}".replace(",", ".")


def tgl(iso):
    try:
        d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return "?"
    bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    return f"{d.day} {bulan[d.month - 1]} {d.year}"


def waktu(iso):
    try:
        return dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def nomor_valid(s):
    if not re.fullmatch(r"#?\d{1,9}", str(s).strip()):
        raise Gagal(f"Nomor pos tidak valid: {s!r} (contoh: 12).", K_INPUT)
    return int(str(s).strip().lstrip("#"))


def slug_tag(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    if not s:
        raise Gagal(f"Nama tag tidak valid: {s!r}", K_INPUT)
    return s


# ---------------------------------------------------------------- pengambilan data
def semua_pos(k, view="all", statuses=None, tags=None, query=None, limit="all"):
    q = {"view": view, "limit": limit}
    if statuses:
        q["statuses"] = ",".join(statuses)
    if tags:
        q["tags"] = ",".join(tags)
    if query:
        q["query"] = query
    hasil = k.minta("GET", "/api/v1/posts", query=q)
    if not isinstance(hasil, list):
        raise Gagal("Bentuk jawaban daftar pos tidak dikenali (versi Fider berbeda?).", K_SERVER)
    return hasil


def satu_pos(k, nomor):
    return k.minta("GET", f"/api/v1/posts/{nomor}")


def daftar_tag(k):
    t = k.minta("GET", "/api/v1/tags")
    return t if isinstance(t, list) else []


def baris_pos(p):
    st = NAMA_STATUS.get(p.get("status"), p.get("status", "?"))
    tg = ",".join(p.get("tags") or []) or "-"
    return (f"#{p['number']:<4} {angka(p.get('votesCount', 0)):>5} suara  "
            f"{angka(p.get('commentsCount', 0)):>3} komentar  [{st}]  {p.get('title', '')}  (tag: {tg})")


def cetak(hasil, args, teks):
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(teks)


PRATINJAU = "PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Setelah pemilik setuju, ulangi perintah yang sama dengan --ya."


# ---------------------------------------------------------------- perintah baca
def cmd_cek(k, args):
    t = k.minta("GET", "/api/v1/tags")
    role = "tidak diketahui"
    try:
        k.minta("GET", "/api/v1/users", query={"limit": "1"})
        role = "Administrator (dapat membaca daftar pengguna)"
    except Gagal as e:
        if e.kode == K_IZIN:
            role = "Collaborator (bukan Administrator: tidak bisa membuat tag baru)"
    total = len(semua_pos(k, "all"))
    teks = (f"OK: Fider terhubung di {k.url}\n- Kunci API   : valid (tidak ditampilkan)\n- Peran akun  : {role}\n"
            f"- Jumlah pos  : {angka(total)} (tidak termasuk duplikat/dihapus)\n- Jumlah tag  : {len(t)}")
    cetak({"ok": True, "url": k.url, "peran": role, "pos": total, "tag": len(t)}, args, teks)
    return K_OK


def cmd_daftar(k, args):
    st = None
    if args.status:
        st = []
        for s in args.status.split(","):
            baku = ALIAS_STATUS.get(s.strip().lower())
            if not baku:
                raise Gagal(f"Status {s!r} tidak dikenal. Pilihan: terbuka, rencana, dikerjakan, selesai, ditolak.", K_INPUT)
            st.append(baku)
    view = {"suara": "most-wanted", "terbaru": "recent", "diskusi": "most-discussed"}[args.urut]
    pos = semua_pos(k, view, st, [slug_tag(t) for t in args.tag.split(",")] if args.tag else None,
                    limit="all")
    if args.urut == "suara":
        pos.sort(key=lambda p: (-p.get("votesCount", 0), p["number"]))
    pos = pos[: args.batas]
    if not pos:
        cetak([], args, "Tidak ada pos yang cocok.")
        return K_OK
    cetak(pos, args, "\n".join(baris_pos(p) for p in pos))
    return K_OK


def cmd_cari(k, args):
    kata = " ".join(args.kata).strip()
    if not kata:
        raise Gagal("Tulis kata yang dicari: cari \"QRIS\"", K_INPUT)
    pos = semua_pos(k, "all", query=kata, limit="30")
    if not pos:
        cetak([], args, f"Tidak ada pos yang mengandung \"{kata}\".")
        return K_OK
    cetak(pos, args, "\n".join(baris_pos(p) for p in pos))
    return K_OK


def cmd_lihat(k, args):
    n = nomor_valid(args.nomor)
    p = satu_pos(k, n)
    kom = k.minta("GET", f"/api/v1/posts/{n}/comments")
    baris = [f"POS #{p['number']}: {p['title']}",
             f"Status : {NAMA_STATUS.get(p.get('status'), p.get('status'))}    Suara: {angka(p.get('votesCount', 0))}    "
             f"Komentar: {angka(p.get('commentsCount', 0))}    Dibuat: {tgl(p.get('createdAt'))}",
             f"Tag    : {', '.join(p.get('tags') or []) or '-'}"]
    r = p.get("response") or {}
    if r.get("text"):
        baris.append(f"Tanggapan tim: {r['text']}")
    if (r.get("original") or {}).get("number"):
        baris.append(f"Digabung ke   : #{r['original']['number']}")
    baris.append("Uraian : " + (rapikan(p.get("description")) or "(kosong)"))
    if isinstance(kom, list) and kom:
        baris.append("Komentar:")
        for c in kom[:10]:
            baris.append(f"  - {c.get('user', {}).get('name', '?')} ({tgl(c.get('createdAt'))}): {rapikan(c.get('content'))}")
    cetak({"pos": p, "komentar": kom}, args, "\n".join(baris))
    return K_OK


def cmd_tag_daftar(k, args):
    t = daftar_tag(k)
    if not t:
        cetak([], args, "Belum ada tag. Buat dengan: tag-buat \"Pembayaran\" --ya")
        return K_OK
    cetak(t, args, "\n".join(f"- {x['name']}  (slug: {x['slug']}, {'publik' if x.get('isPublic') else 'privat'})" for x in t))
    return K_OK


def cmd_ringkasan(k, args):
    """Ringkasan mingguan: pos teratas berdasarkan suara + suara baru dalam N hari (butuh peran Collaborator)."""
    sekarang = dt.datetime.now(dt.timezone.utc)
    awal = sekarang - dt.timedelta(days=args.hari)
    aktif = semua_pos(k, "all", ["open", "planned", "started"])
    selesai = semua_pos(k, "all", ["completed"])
    aktif.sort(key=lambda p: (-p.get("votesCount", 0), p["number"]))
    baru = [p for p in aktif + selesai + semua_pos(k, "all", ["declined"])
            if (waktu(p.get("createdAt")) or awal) >= awal]
    selesai_baru = [p for p in selesai if (waktu((p.get("response") or {}).get("respondedAt")) or awal - dt.timedelta(1)) >= awal]
    top = aktif[: args.top]
    suara_baru, catatan = {}, []
    for p in top:
        try:
            v = k.minta("GET", f"/api/v1/posts/{p['number']}/votes")
        except Gagal as e:
            if e.kode == K_IZIN:
                catatan.append("Suara baru per pos tidak bisa dihitung (butuh peran Collaborator/Administrator).")
                break
            raise
        suara_baru[p["number"]] = sum(1 for x in v if (waktu(x.get("createdAt")) or awal - dt.timedelta(1)) >= awal)
    total_suara = sum(p.get("votesCount", 0) for p in aktif)
    baris = [f"RINGKASAN MASUKAN PELANGGAN - {args.hari} hari terakhir (per {tgl(sekarang.isoformat())})",
             f"- Pos aktif (terbuka/direncanakan/dikerjakan): {angka(len(aktif))}, total {angka(total_suara)} suara",
             f"- Pos baru minggu ini: {angka(len(baru))}",
             f"- Ditandai selesai minggu ini: {angka(len(selesai_baru))}", "",
             f"TOP {len(top)} SUARA TERBANYAK"]
    if not top:
        baris.append("  (belum ada pos aktif)")
    for i, p in enumerate(top, 1):
        tambahan = f"  (+{suara_baru[p['number']]} minggu ini)" if p["number"] in suara_baru else ""
        baris.append(f"{i}. #{p['number']} {p['title']} - {angka(p.get('votesCount', 0))} suara{tambahan}"
                     f" [{NAMA_STATUS.get(p.get('status'))}]")
    if baru:
        baris += ["", "POS BARU"] + [f"- #{p['number']} {p['title']} ({angka(p.get('votesCount', 0))} suara)" for p in baru[:10]]
    if selesai_baru:
        baris += ["", "BARU SELESAI"] + [f"- #{p['number']} {p['title']}" for p in selesai_baru[:10]]
    baris += [""] + catatan
    baris.append("Catatan: angka dari Fider apa adanya; suara pemilik/tim ikut terhitung.")
    hasil = {"hari": args.hari, "aktif": len(aktif), "total_suara": total_suara, "baru": [p["number"] for p in baru],
             "selesai_baru": [p["number"] for p in selesai_baru],
             "top": [{"nomor": p["number"], "judul": p["title"], "suara": p.get("votesCount", 0),
                      "suara_baru": suara_baru.get(p["number"])} for p in top]}
    cetak(hasil, args, "\n".join(baris).rstrip())
    return K_OK


def buat_draf(p, gaya, catatan):
    judul = p["title"]
    nama_hal = rapikan(judul)
    suara = p.get("votesCount", 0)
    if gaya == "santai":
        buka = "Halo Kak, kabar baik!"
        inti = f"Usulan \"{nama_hal}\" sekarang sudah kami kerjakan dan bisa dipakai."
        tutup = "Terima kasih sudah ikut memberi masukan. Kalau masih ada yang kurang pas, kabari kami ya."
    else:
        buka = "Selamat siang,"
        inti = f"Kami informasikan bahwa usulan \"{nama_hal}\" telah selesai kami perbaiki/tambahkan."
        tutup = "Terima kasih atas masukan Anda. Jika masih ada kendala, silakan sampaikan kembali kepada kami."
    baris = [buka, inti]
    if catatan:
        baris.append(catatan.strip())
    if suara >= 2:
        baris.append(f"Usulan ini didukung {angka(suara)} orang, terima kasih untuk semuanya.")
    baris.append(tutup)
    return "\n".join(baris)


def cmd_draf(k, args):
    n = nomor_valid(args.nomor)
    p = satu_pos(k, n)
    peringatan = ""
    if p.get("status") != "completed":
        peringatan = (f"PERINGATAN: pos #{n} berstatus \"{NAMA_STATUS.get(p.get('status'))}\", belum \"Selesai\". "
                      "Pastikan perbaikannya benar-benar sudah jalan sebelum draf ini dikirim.\n\n")
    draf = buat_draf(p, args.gaya, args.catatan)
    teks = (peringatan + f"DRAF BALASAN untuk pos #{n} (belum dikirim ke siapa pun; pemilik yang mengirim/menempel):\n"
            f"------------------------------\n{draf}\n------------------------------\n"
            "Untuk menempelkannya sebagai komentar publik di Fider: komentar " + str(n) + " --teks \"...\" --ya")
    cetak({"nomor": n, "status": p.get("status"), "draf": draf, "perlu_periksa": bool(peringatan)}, args, teks)
    return K_OK


# ---------------------------------------------------------------- perintah tulis
def wajib_ya(args, ringkas, hasil=None):
    """Tampilkan pratinjau bila belum --ya. Kembalikan True bila boleh menulis."""
    if args.ya:
        return True
    cetak({"pratinjau": True, **(hasil or {})}, args, f"{ringkas}\n\n{PRATINJAU}")
    return False


def baca_catatan(path):
    """Baca catatan mentah (txt/md: dipisah baris kosong atau butir '-', '*', '1.'; atau .json)."""
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as f:
            teks = f.read()
    except OSError as e:
        raise Gagal(f"Tidak bisa membaca berkas catatan {path}: {e.strerror}", K_FILE)
    except UnicodeDecodeError:
        raise Gagal(f"Berkas {path} bukan teks UTF-8. Simpan ulang sebagai UTF-8.", K_FILE)
    if not teks.strip():
        raise Gagal(f"Berkas {path} kosong.", K_FILE)
    if path.lower().endswith(".json"):
        try:
            data = json.loads(teks)
        except ValueError as e:
            raise Gagal(f"JSON rusak di {path}: {e}", K_FILE)
        if not isinstance(data, list):
            raise Gagal("JSON harus berupa daftar objek [{\"judul\":..., \"uraian\":..., \"tag\":[...]}].", K_FILE)
        butir = []
        for i, x in enumerate(data, 1):
            if not isinstance(x, dict) or not rapikan(str(x.get("judul", ""))):
                raise Gagal(f"Butir ke-{i} di JSON tidak punya 'judul'.", K_FILE)
            tag = x.get("tag") or []
            if isinstance(tag, str):
                tag = [t for t in tag.split(",") if t.strip()]
            butir.append({"judul": str(x["judul"]), "uraian": str(x.get("uraian", "")),
                          "tag": [str(t) for t in tag], "pelanggan": x.get("pelanggan")})
        return butir
    butir, sekarang = [], []
    for baris in teks.replace("\r\n", "\n").split("\n"):
        b = baris.strip()
        mulai_butir = re.match(r"^([-*•]|\d+[.)])\s+", b)
        if not b:
            if sekarang:
                butir.append(sekarang)
                sekarang = []
        elif mulai_butir and sekarang:
            butir.append(sekarang)
            sekarang = [re.sub(r"^([-*•]|\d+[.)])\s+", "", b)]
        else:
            sekarang.append(re.sub(r"^([-*•]|\d+[.)])\s+", "", b))
    if sekarang:
        butir.append(sekarang)
    hasil = []
    for bl in butir:
        judul, sisa = bl[0], " ".join(bl[1:])
        hasil.append({"judul": judul, "uraian": sisa, "tag": [], "pelanggan": None})
    return hasil


def siapkan_impor(butir, sumber, ada, tetap):
    """Bersihkan, samarkan data pribadi, dan tandai kemungkinan duplikat."""
    rencana, terlihat = [], []
    for b in butir:
        judul, n1 = samarkan_pribadi(rapikan(b["judul"]))
        uraian, n2 = samarkan_pribadi(b["uraian"].strip())
        judul_akhir = potong(judul, BATAS_JUDUL)
        if len(judul) > BATAS_JUDUL and not uraian:
            uraian = judul
        elif len(judul) > BATAS_JUDUL:
            uraian = judul + "\n\n" + uraian
        tambahan = []
        if b.get("pelanggan"):
            try:
                tambahan.append(f"Dilaporkan oleh sekitar {angka(int(b['pelanggan']))} pelanggan.")
            except (ValueError, TypeError):
                raise Gagal(f"'pelanggan' harus angka (butir: {judul_akhir!r}).", K_FILE)
        if sumber:
            tambahan.append(f"Sumber: {sumber}.")
        uraian_akhir = (uraian + ("\n\n" if uraian and tambahan else "") + " ".join(tambahan)).strip()
        mirip, skor = None, 0.0
        for p in ada + terlihat:
            s = kemiripan(judul_akhir, p["title"] if "title" in p else p["judul"])
            if s > skor:
                skor, mirip = s, p
        aksi = "buat"
        if mirip and skor >= 0.6:
            aksi = "buat" if tetap else "lewati"
        rencana.append({"judul": judul_akhir, "uraian": uraian_akhir, "tag": b.get("tag", []),
                        "disamarkan": n1 + n2, "aksi": aksi,
                        "mirip_dengan": ({"nomor": mirip.get("number"), "judul": mirip.get("title", mirip.get("judul")),
                                          "skor": round(skor, 2)} if mirip and skor >= 0.6 else None)})
        terlihat.append({"judul": judul_akhir})
    return rencana


def cmd_impor(k, args):
    butir = baca_catatan(args.berkas)
    if len(butir) > BATAS_IMPOR:
        raise Gagal(f"Terlalu banyak butir ({len(butir)}); maksimum {BATAS_IMPOR} per impor. Pecah berkasnya.", K_INPUT)
    ada = semua_pos(k, "all")
    rencana = siapkan_impor(butir, args.sumber, ada, args.tetap)
    tag_ada = {t["slug"] for t in daftar_tag(k)}
    tag_hilang = sorted({slug_tag(t) for r in rencana for t in r["tag"]} - tag_ada)
    baris = [f"RENCANA IMPOR dari {os.path.basename(args.berkas)}: {len(rencana)} butir"]
    for i, r in enumerate(rencana, 1):
        cap = "BUAT  " if r["aksi"] == "buat" else "LEWATI"
        baris.append(f"{i}. [{cap}] {r['judul']}")
        if r["uraian"]:
            baris.append(f"      uraian: {potong(r['uraian'], 90)}")
        if r["mirip_dengan"]:
            m = r["mirip_dengan"]
            acuan = f"#{m['nomor']}" if m["nomor"] else "butir lain di berkas ini"
            baris.append(f"      mirip dengan {acuan} \"{m['judul']}\" (kemiripan {int(m['skor'] * 100)}%)"
                         + ("" if r["aksi"] == "lewati" else " - tetap dibuat (--tetap)"))
        if r["disamarkan"]:
            baris.append(f"      {r['disamarkan']} nomor HP/email disembunyikan (papan Fider biasanya publik)")
        if r["tag"]:
            baris.append(f"      tag: {', '.join(r['tag'])}")
    if tag_hilang:
        baris.append(f"Tag belum ada di Fider: {', '.join(tag_hilang)} (dilewati saat menandai; buat dulu dengan tag-buat)")
    baris.append("Catatan: pos yang dibuat lewat kunci API otomatis mendapat 1 suara dari pemilik kunci"
                 + (" (akan dihapus, --hapus-suara-saya)." if args.hapus_suara_saya else "."))
    if not wajib_ya(args, "\n".join(baris), {"rencana": rencana, "tag_belum_ada": tag_hilang}):
        return K_OK
    dibuat, lewati = [], 0
    for r in rencana:
        if r["aksi"] == "lewati":
            lewati += 1
            continue
        res = k.minta("POST", "/api/v1/posts", {"title": r["judul"], "description": r["uraian"]})
        no = res.get("number")
        if not no:
            raise Gagal("Fider tidak mengembalikan nomor pos baru.", K_SERVER)
        if args.hapus_suara_saya:
            k.minta("DELETE", f"/api/v1/posts/{no}/votes")
        for t in r["tag"]:
            s = slug_tag(t)
            if s in tag_ada:
                k.minta("POST", f"/api/v1/posts/{no}/tags/{s}")
        dibuat.append({"nomor": no, "judul": r["judul"]})
        time.sleep(args.jeda)
    teks = f"SELESAI: {len(dibuat)} pos dibuat, {lewati} dilewati (kemungkinan duplikat).\n" + \
        "\n".join(f"- #{d['nomor']} {d['judul']}" for d in dibuat)
    cetak({"dibuat": dibuat, "dilewati": lewati}, args, teks)
    return K_OK


def cmd_tag_buat(k, args):
    nama = rapikan(args.nama)
    if not nama or len(nama) > 30:
        raise Gagal("Nama tag 1-30 karakter.", K_INPUT)
    warna = args.warna.lstrip("#").upper()
    if not re.fullmatch(r"[0-9A-F]{6}", warna):
        raise Gagal("Warna harus 6 digit hex tanpa '#', mis. 3B82F6.", K_INPUT)
    if slug_tag(nama) in {t["slug"] for t in daftar_tag(k)}:
        cetak({"sudah_ada": True}, args, f"Tag \"{nama}\" sudah ada; tidak ada yang diubah.")
        return K_OK
    if not wajib_ya(args, f"Akan membuat tag \"{nama}\" (warna #{warna}, {'privat' if args.privat else 'publik'}).",
                    {"nama": nama}):
        return K_OK
    t = k.minta("POST", "/api/v1/tags", {"name": nama, "color": warna, "isPublic": not args.privat})
    cetak(t, args, f"Tag dibuat: {t.get('name')} (slug: {t.get('slug')})")
    return K_OK


def cmd_tag(k, args):
    n = nomor_valid(args.nomor)
    p = satu_pos(k, n)
    slugs = [slug_tag(t) for t in args.nama.split(",") if t.strip()]
    if not slugs:
        raise Gagal("Tulis nama tag: tag 12 pembayaran,fitur", K_INPUT)
    ada = {t["slug"] for t in daftar_tag(k)}
    hilang = [s for s in slugs if s not in ada]
    if hilang:
        raise Gagal(f"Tag belum ada: {', '.join(hilang)}. Buat dulu: tag-buat \"{hilang[0]}\" --ya "
                    "(butuh Administrator). Daftar tag: tag-daftar.", K_INPUT)
    aksi = "MELEPAS" if args.lepas else "MEMASANG"
    if not wajib_ya(args, f"Akan {aksi} tag {', '.join(slugs)} pada pos #{n} \"{p['title']}\" (tag saat ini: "
                          f"{', '.join(p.get('tags') or []) or '-'}).", {"nomor": n, "tag": slugs}):
        return K_OK
    for s in slugs:
        k.minta("DELETE" if args.lepas else "POST", f"/api/v1/posts/{n}/tags/{s}")
    cetak({"nomor": n, "tag": slugs}, args, f"SELESAI: tag {', '.join(slugs)} {'dilepas dari' if args.lepas else 'dipasang pada'} pos #{n}.")
    return K_OK


def cmd_gabung(k, args):
    dup, asli = nomor_valid(args.duplikat), nomor_valid(args.asli)
    if dup == asli:
        raise Gagal("Pos tidak bisa digabung ke dirinya sendiri.", K_INPUT)
    pd, pa = satu_pos(k, dup), satu_pos(k, asli)
    if pa.get("status") == "duplicate":
        raise Gagal(f"Pos #{asli} sendiri sudah berstatus duplikat. Pilih pos induk yang lain.", K_INPUT)
    ringkas = (f"Akan menandai pos #{dup} \"{pd['title']}\" ({angka(pd.get('votesCount', 0))} suara) sebagai DUPLIKAT dari "
               f"#{asli} \"{pa['title']}\" ({angka(pa.get('votesCount', 0))} suara).\n"
               "Pos duplikat hilang dari daftar utama dan suaranya dipindahkan ke pos induk oleh Fider.")
    if not wajib_ya(args, ringkas, {"duplikat": dup, "asli": asli}):
        return K_OK
    k.minta("PUT", f"/api/v1/posts/{dup}/status", {"status": "duplicate", "originalNumber": asli,
                                                     "text": args.catatan or ""})
    sesudah = satu_pos(k, asli)
    cetak({"duplikat": dup, "asli": asli, "suara_asli": sesudah.get("votesCount")}, args,
          f"SELESAI: #{dup} digabung ke #{asli}. Suara #{asli} sekarang {angka(sesudah.get('votesCount', 0))}.")
    return K_OK


def cmd_status(k, args):
    n = nomor_valid(args.nomor)
    baku = ALIAS_STATUS.get(args.status.strip().lower())
    if not baku:
        raise Gagal(f"Status {args.status!r} tidak dikenal. Pilihan: terbuka, rencana, dikerjakan, selesai, ditolak. "
                    "(Untuk duplikat pakai perintah gabung.) Fider diam-diam menganggap status asing sebagai 'terbuka', "
                    "jadi script menolaknya di sini.", K_INPUT)
    p = satu_pos(k, n)
    if p.get("status") == "duplicate":
        raise Gagal(f"Pos #{n} berstatus duplikat; ubah pos induknya, bukan yang ini.", K_INPUT)
    ringkas = (f"Akan mengubah status pos #{n} \"{p['title']}\": {NAMA_STATUS.get(p.get('status'))} -> {NAMA_STATUS[baku]}."
               + (f"\nTeks tanggapan publik: \"{args.catatan}\"" if args.catatan else "\n(tanpa teks tanggapan)"))
    if baku in ("completed", "declined") and not args.catatan:
        ringkas += "\nSaran: tambahkan --catatan agar pelanggan yang memberi suara tahu alasannya."
    if not wajib_ya(args, ringkas, {"nomor": n, "status": baku}):
        return K_OK
    k.minta("PUT", f"/api/v1/posts/{n}/status", {"status": baku, "text": args.catatan or ""})
    sesudah = satu_pos(k, n)
    if sesudah.get("status") != baku:
        raise Gagal(f"Fider tidak menerapkan status {baku} (status sekarang {sesudah.get('status')}).", K_SERVER)
    msg = f"SELESAI: pos #{n} sekarang \"{NAMA_STATUS[baku]}\"."
    if baku == "completed":
        msg += f"\nUntuk balasan ke pelanggan: draf-balasan {n}"
    cetak({"nomor": n, "status": baku}, args, msg)
    return K_OK


def cmd_komentar(k, args):
    n = nomor_valid(args.nomor)
    teks = args.teks.strip()
    if not teks:
        raise Gagal("Teks komentar kosong.", K_INPUT)
    if len(teks) > 5000:
        raise Gagal("Komentar terlalu panjang (maks. 5.000 karakter).", K_INPUT)
    teks2, nsam = samarkan_pribadi(teks)
    p = satu_pos(k, n)
    ringkas = (f"Akan menulis komentar PUBLIK pada pos #{n} \"{p['title']}\" atas nama akun pemilik kunci:\n---\n{teks2}\n---"
               + (f"\n({nsam} nomor HP/email disembunyikan.)" if nsam else ""))
    if not wajib_ya(args, ringkas, {"nomor": n}):
        return K_OK
    r = k.minta("POST", f"/api/v1/posts/{n}/comments", {"content": teks2})
    cetak({"nomor": n, "komentar_id": r.get("id")}, args, f"SELESAI: komentar ditulis di pos #{n}.")
    return K_OK


PERINTAH = {
    "cek": cmd_cek, "daftar": cmd_daftar, "cari": cmd_cari, "lihat": cmd_lihat, "tag-daftar": cmd_tag_daftar,
    "ringkasan-mingguan": cmd_ringkasan, "draf-balasan": cmd_draf, "impor": cmd_impor, "tag": cmd_tag,
    "tag-buat": cmd_tag_buat, "gabung": cmd_gabung, "status": cmd_status, "komentar": cmd_komentar,
}


def buat_parser():
    ap = argparse.ArgumentParser(prog="fider.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--versi", action="version", version=VERSI)
    sub = ap.add_subparsers(dest="perintah", required=True)

    def umum(p, tulis=False):
        p.add_argument("--url", help="alamat Fider (bawaan: ENV FIDER_URL, file alamat, atau http://localhost:3000)")
        p.add_argument("--kunci-file", help="file berisi kunci API (bawaan: ENV FIDER_API_KEY / ~/.komunitech/fider-kunci.txt)")
        p.add_argument("--json", action="store_true", help="hasil JSON")
        if tulis:
            p.add_argument("--ya", action="store_true", help="benar-benar menulis (tanpa ini hanya pratinjau)")
        return p

    p = sub.add_parser("simpan-kunci"); p.add_argument("--kunci-file"); p.add_argument("--ya", action="store_true")
    p = sub.add_parser("simpan-alamat"); p.add_argument("alamat", nargs="?")
    umum(sub.add_parser("cek"))
    p = umum(sub.add_parser("daftar"))
    p.add_argument("--status", help="terbuka,rencana,dikerjakan,selesai,ditolak (pisah koma)")
    p.add_argument("--tag"); p.add_argument("--urut", choices=["suara", "terbaru", "diskusi"], default="suara")
    p.add_argument("--batas", type=int, default=20)
    p = umum(sub.add_parser("cari")); p.add_argument("kata", nargs="+")
    p = umum(sub.add_parser("lihat")); p.add_argument("nomor")
    umum(sub.add_parser("tag-daftar"))
    p = umum(sub.add_parser("ringkasan-mingguan"))
    p.add_argument("--hari", type=int, default=7); p.add_argument("--top", type=int, default=5)
    p = umum(sub.add_parser("draf-balasan")); p.add_argument("nomor")
    p.add_argument("--gaya", choices=["sopan", "santai"], default="sopan"); p.add_argument("--catatan", default="")
    p = umum(sub.add_parser("impor"), True); p.add_argument("berkas")
    p.add_argument("--sumber", default="", help="mis. 'WhatsApp pelanggan' atau 'ulasan Shopee'")
    p.add_argument("--tetap", action="store_true", help="tetap buat walau mirip pos lama")
    p.add_argument("--hapus-suara-saya", action="store_true"); p.add_argument("--jeda", type=float, default=0.2)
    p = umum(sub.add_parser("tag"), True); p.add_argument("nomor"); p.add_argument("nama", help="satu atau beberapa, pisah koma")
    p.add_argument("--lepas", action="store_true")
    p = umum(sub.add_parser("tag-buat"), True); p.add_argument("nama"); p.add_argument("--warna", default="3B82F6")
    p.add_argument("--privat", action="store_true")
    p = umum(sub.add_parser("gabung"), True); p.add_argument("duplikat"); p.add_argument("asli"); p.add_argument("--catatan", default="")
    p = umum(sub.add_parser("status"), True); p.add_argument("nomor"); p.add_argument("status")
    p.add_argument("--catatan", default="")
    p = umum(sub.add_parser("komentar"), True); p.add_argument("nomor"); p.add_argument("--teks", required=True)
    return ap


def main(argv=None):
    args = buat_parser().parse_args(argv)
    kunci = ""
    try:
        if args.perintah == "simpan-kunci":
            return simpan_kunci(args)
        if args.perintah == "simpan-alamat":
            return simpan_alamat(args)
        url, _ = alamat_awal(args)
        periksa_url(url)
        kunci = ambil_kunci(args)
        if re.search(r"\s", kunci):
            raise Gagal("Kunci API berisi spasi/baris baru; simpan ulang dengan simpan-kunci --ya.", K_KUNCI)
        if getattr(args, "batas", 1) < 1 or getattr(args, "hari", 1) < 1 or getattr(args, "top", 1) < 1:
            raise Gagal("--batas/--hari/--top minimal 1.", K_INPUT)
        return PERINTAH[args.perintah](Klien(url, kunci), args)
    except Gagal as e:
        sys.stderr.write(samarkan(f"GALAT: {e}", kunci) + "\n")
        return e.kode
    except KeyboardInterrupt:
        sys.stderr.write("Dibatalkan.\n")
        return 130
    except BrokenPipeError:
        return K_OK


if __name__ == "__main__":
    sys.exit(main())
