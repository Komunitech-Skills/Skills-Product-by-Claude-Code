#!/usr/bin/env python3
"""Asisten SiYuan lokal untuk basis pengetahuan usaha (Komunitech) - memakai kernel API resmi SiYuan.

Hanya Python standar (urllib). Lintas OS: macOS/Linux `python3`, Windows `python` atau `py`.

Prinsip keamanan:
- Alamat kernel selain 127.0.0.1/::1 (komputer ini) DITOLAK kecuali `--izinkan-jarak-jauh`, dan
  alamat internet wajib https.
- Token API dibaca dari `--kunci-file` (selalu menang), ENV `SIYUAN_TOKEN`, ENV `SIYUAN_TOKEN_FILE`,
  atau file lokal default berizin ketat; tidak pernah dicetak (disamarkan) di keluaran mana pun.
- Membuat dokumen tidak pernah menimpa dokumen yang sudah ada di path yang sama tanpa `--timpa`
  (dan `--timpa` tetap butuh `--ya`). Menambah isi (`tambah`) hanya menambahkan blok baru, tidak
  pernah mengganti isi lama.
- Pencarian & daftar dokumen lama memakai kernel API `/api/query/sql` lewat TEMPLATE SELECT tetap
  yang sudah ditulis di script ini (lihat SQL_CARI/SQL_LAMA). Kata kunci pengguna hanya disisipkan
  di dalam literal string SQL setelah tanda kutip tunggal digandakan (aturan escaping SQLite yang
  baku) - tidak pernah ada SQL bebas dari pengguna yang dikirim ke kernel.
- Kernel SiYuan tidak boleh dipasang port-forward/dibuka ke internet; lihat docs/panduan-siyuan.md.

Perintah:
  cek                                  koneksi, token, daftar buku catatan
  simpan-kunci                         simpan token API ke file lokal (izin 600)
  daftar-buku                          daftar buku catatan (notebook)
  cari KATA                            cari teks di semua dokumen (judul + path + cuplikan)
  baca (--id ID | --notebook ID --path /jalur)   baca isi dokumen sebagai Markdown
  buat --notebook ID --path /jalur (--md TEKS | --md-file FILE | --md -)   buat dokumen baru
                                        (--timpa: cadangan isi lama ke ~/KomunitechData/siyuan/cadangan/,
                                        path absolut dicetak; ubah dengan --cadangan-dir)
  tambah --id ID (--md TEKS | --md-file FILE | --md -)   tambah isi ke dokumen/blok yang sudah ada
  lama [--hari N] [--notebook ID]      dokumen yang belum diperbarui > N hari (default 90)
  ekspor-basis --notebook ID [--file F] [--filter KATA]   gabungkan semua dokumen 1 buku catatan
                                        jadi satu file Markdown (basis pengetahuan untuk skill CS)

Kode keluar: 0 berhasil | 2 argumen/input salah | 3 kernel SiYuan tidak bisa dihubungi |
5 token salah/kurang hak (401/403) atau alamat bukan localhost tanpa izin | 6 galat lain dari kernel |
7 tidak dibuat karena sudah ada dokumen di path itu (perlu --timpa) | 8 saat menulis: koneksi
putus/jawaban terpotong/galat server 5xx - data mungkin sudah (sebagian) tersimpan, JANGAN diulang
begitu saja, cek di aplikasi SiYuan dulu.
"""
import argparse
import datetime as dt
import http.client
import ipaddress
import json
import os
import re
import socket
import stat
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

VERSI_SKRIP = "1.0.11"
URL_DEFAULT = "http://127.0.0.1:6806"
BATAS_WAKTU = 20
FILE_KUNCI_DEFAULT = os.path.expanduser(os.path.join("~", ".komunitech", "siyuan-kunci.txt"))
PER_HALAMAN_SNIPPET = 400


def folder_cadangan_default():
    """v1.0.10: cadangan isi lama disimpan di folder data pengguna, DI LUAR folder skill (agar tidak ikut
    terhapus saat skill diperbarui/diinstal ulang), konsisten dengan skill Komunitech lain. Urutan:
    ENV KOMUNITECH_SIYUAN_CADANGAN -> ENV KOMUNITECH_DATA/siyuan/cadangan -> ~/KomunitechData/siyuan/cadangan."""
    env = os.environ.get("KOMUNITECH_SIYUAN_CADANGAN")
    if env:
        return os.path.abspath(os.path.expanduser(env))
    data = os.environ.get("KOMUNITECH_DATA")
    if data:
        return os.path.abspath(os.path.join(os.path.expanduser(data), "siyuan", "cadangan"))
    return os.path.join(os.path.expanduser("~"), "KomunitechData", "siyuan", "cadangan")


def _folder_cadangan(folder_cadangan=None):
    """Folder cadangan sebagai path ABSOLUT (dari --cadangan-dir bila diisi, selain itu default)."""
    if folder_cadangan:
        return os.path.abspath(os.path.expanduser(folder_cadangan))
    return folder_cadangan_default()

KELUAR_ARG, KELUAR_KONEKSI, KELUAR_AKSES, KELUAR_LAIN, KELUAR_DOBEL, KELUAR_TIDAK_PASTI = 2, 3, 5, 6, 7, 8

_RAHASIA = []  # nilai yang wajib disamarkan dari semua keluaran (token API)


# ------------------------------------------------------------------ utilitas umum
class Gagal(Exception):
    def __init__(self, pesan, kode=KELUAR_LAIN, saran=None, mungkin_terkirim=False):
        super().__init__(pesan)
        self.pesan = pesan
        self.kode = kode
        self.saran = saran
        self.mungkin_terkirim = mungkin_terkirim  # True = permintaan TULIS mungkin sudah sampai


def samarkan_token(t):
    if not t:
        return "(kosong)"
    return "****" + t[-4:] if len(t) >= 8 else "****"


def samarkan(teks):
    teks = str(teks)
    for r in _RAHASIA:
        if r and r in teks:
            teks = teks.replace(r, samarkan_token(r))
    return teks


def cetak(teks="", file=None):
    print(samarkan(teks), file=file or sys.stdout)


def escape_sql_literal(nilai):
    """Aturan escaping literal string SQLite yang baku: gandakan tanda kutip tunggal.

    Ini BUKAN pembangun SQL bebas: fungsi ini hanya boleh dipakai untuk mengisi bagian
    '...' di dalam TEMPLATE SELECT tetap (SQL_CARI/SQL_LAMA) di bawah. Karakter kontrol
    dan byte NUL dibuang, dan panjang dibatasi supaya permintaan tidak raksasa."""
    if nilai is None:
        nilai = ""
    nilai = str(nilai).replace("\x00", "")
    nilai = "".join(c for c in nilai if c == "\n" or c == "\t" or unicodedata.category(c)[0] != "C")
    nilai = nilai[:200]
    return nilai.replace("'", "''")


def baca_teks_masukan(teks, dari_file, dari_stdin_flag):
    """Ambil isi Markdown dari salah satu dari --md/--md-file/'-' (stdin). Persis satu wajib diisi."""
    sumber = [x for x in (teks is not None, bool(dari_file), dari_stdin_flag) if x]
    if len(sumber) == 0:
        raise Gagal("Isi Markdown belum diisi. Pakai --md \"teks\", --md-file file.md, atau --md -.", KELUAR_ARG)
    if len(sumber) > 1:
        raise Gagal("Isi Markdown hanya boleh dari satu sumber (--md / --md-file / --md -).", KELUAR_ARG)
    if dari_stdin_flag:
        return sys.stdin.read()
    if dari_file:
        try:
            with open(dari_file, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            raise Gagal(f"Tidak bisa membaca file '{dari_file}': {e}", KELUAR_ARG) from e
    return teks


def potong_cuplikan(teks, kata, panjang=PER_HALAMAN_SNIPPET):
    teks = re.sub(r"\s+", " ", str(teks or "")).strip()
    if not teks:
        return "(kosong)"
    idx = teks.lower().find(kata.lower()) if kata else -1
    if idx == -1:
        return teks[:panjang] + ("..." if len(teks) > panjang else "")
    mulai = max(0, idx - panjang // 3)
    akhir = min(len(teks), idx + len(kata) + panjang // 2)
    hasil = teks[mulai:akhir]
    return ("..." if mulai > 0 else "") + hasil + ("..." if akhir < len(teks) else "")


# ------------------------------------------------------------------ token & alamat
def simpan_kunci_ke_file(path, token, paksa):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    if os.path.exists(path) and not paksa:
        raise Gagal(
            f"File kunci '{path}' sudah ada. Jalankan lagi dengan --ya untuk menimpa, "
            "atau pakai --kunci-file lain untuk menyimpan token kedua.",
            KELUAR_ARG,
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write(token.strip() + "\n")
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass  # Windows tanpa dukungan chmod POSIX; tidak fatal


def cek_izin_file_kunci(path):
    try:
        mode = stat.S_IMODE(os.stat(path).st_mode)
    except OSError:
        return
    if os.name == "posix" and (mode & (stat.S_IRWXG | stat.S_IRWXO)):
        cetak(f"PERINGATAN: file kunci '{path}' bisa dibaca pengguna lain di komputer ini. "
              f"Jalankan: chmod 600 {path}")


def _baca_file_kunci(p, asal):
    try:
        with open(p, "r", encoding="utf-8") as f:
            isi = f.read().strip()
    except OSError as e:
        raise Gagal(f"File kunci ({asal}) '{p}' tidak ditemukan/kosong: {e}", KELUAR_AKSES) from e
    if not isi:
        raise Gagal(f"File kunci '{p}' kosong.", KELUAR_AKSES)
    return isi


def ambil_token(args):
    """Prioritas: --kunci-file > file kunci tersimpan (simpan-kunci) > ENV SIYUAN_TOKEN_FILE > ENV SIYUAN_TOKEN.
    Kunci tersimpan SELALU menang atas token di ENV (token ENV bisa berasal dari token yang ditempel di chat)."""
    dipakai = None
    sumber = None
    if args.kunci_file:
        cek_izin_file_kunci(args.kunci_file)
        dipakai, sumber = _baca_file_kunci(args.kunci_file, "dari --kunci-file"), "--kunci-file"
    elif os.path.exists(FILE_KUNCI_DEFAULT):
        cek_izin_file_kunci(FILE_KUNCI_DEFAULT)
        dipakai, sumber = _baca_file_kunci(FILE_KUNCI_DEFAULT, "tersimpan"), FILE_KUNCI_DEFAULT
    elif os.environ.get("SIYUAN_TOKEN_FILE"):
        p = os.environ["SIYUAN_TOKEN_FILE"]
        dipakai, sumber = _baca_file_kunci(p, "dari ENV SIYUAN_TOKEN_FILE"), "ENV SIYUAN_TOKEN_FILE"
    elif os.environ.get("SIYUAN_TOKEN"):
        dipakai, sumber = os.environ["SIYUAN_TOKEN"], "ENV SIYUAN_TOKEN"
    if sumber in ("--kunci-file", FILE_KUNCI_DEFAULT, "ENV SIYUAN_TOKEN_FILE") and os.environ.get("SIYUAN_TOKEN"):
        cetak(f"PERINGATAN: ENV SIYUAN_TOKEN juga terisi tapi DIABAIKAN; yang dipakai kunci tersimpan ({sumber}). "
              "Jangan menempel token di chat; bila token pernah tertempel, ganti di SiYuan lalu jalankan simpan-kunci --ya.")
    if not dipakai:
        raise Gagal(
            "Token API SiYuan belum diatur. Jalankan dulu: "
            "python3 <folder-skill>/scripts/siyuan.py simpan-kunci "
            "(token dilihat di SiYuan: Settings > Authentication/About > API token).",
            KELUAR_AKSES,
        )
    if re.search(r"\s", dipakai):
        raise Gagal("Token API berisi spasi/baris baru - kemungkinan tersalin rusak. Salin ulang & simpan lagi.",
                     KELUAR_AKSES)
    _RAHASIA.append(dipakai)
    return dipakai


def periksa_alamat(url, izinkan_jarak_jauh):
    u = urllib.parse.urlparse(url)
    host = u.hostname or ""
    try:
        infos = socket.getaddrinfo(host, None)
        ip_list = [ipaddress.ip_address(i[4][0]) for i in infos]
    except (socket.gaierror, ValueError):
        ip_list = []
    lokal = host in ("localhost",) or all(ip.is_loopback for ip in ip_list) if ip_list else host == "localhost"
    if not lokal and not izinkan_jarak_jauh:
        raise Gagal(
            f"Alamat '{url}' bukan komputer ini (localhost/127.0.0.1). Skill ini menolak alamat "
            "jarak jauh secara default (kernel SiYuan JANGAN pernah dibuka ke internet/di-port-forward). "
            "Yakin ini server SiYuan milik Anda sendiri? Tambahkan --izinkan-jarak-jauh.",
            KELUAR_AKSES,
        )
    if not lokal and u.scheme != "https":
        raise Gagal(f"Alamat jarak jauh '{url}' wajib https (bukan http).", KELUAR_AKSES)
    return lokal


# ------------------------------------------------------------------ HTTP ke kernel
def panggil(url_dasar, token, path, payload, lokal, batas_waktu=BATAS_WAKTU):
    data = json.dumps(payload if payload is not None else {}).encode("utf-8")
    req = urllib.request.Request(
        url_dasar.rstrip("/") + path,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Token " + token},
    )
    # Alamat lokal: jangan pernah lewat proxy sistem (token tidak boleh terkirim ke pihak ketiga).
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if lokal else urllib.request.build_opener()
    try:
        with opener.open(req, timeout=batas_waktu) as r:
            mentah = r.read()
    except urllib.error.HTTPError as e:
        badan = e.read()
        try:
            j = json.loads(badan.decode("utf-8", "replace"))
        except (ValueError, UnicodeDecodeError):
            j = None
        if e.code in (401, 403):
            raise Gagal("Token API ditolak SiYuan (401/403). Token salah/sudah diganti - jalankan simpan-kunci lagi.",
                        KELUAR_AKSES) from e
        if 500 <= e.code < 600:
            raise Gagal(f"Kernel SiYuan membalas galat server {e.code} saat memproses permintaan.",
                        KELUAR_TIDAK_PASTI, mungkin_terkirim=True) from e
        pesan = (j or {}).get("msg") if isinstance(j, dict) else None
        raise Gagal(f"Kernel SiYuan menolak permintaan (HTTP {e.code}){': ' + pesan if pesan else ''}.",
                    KELUAR_LAIN) from e
    except (http.client.HTTPException,) as e:
        raise Gagal(f"Jawaban kernel SiYuan terpotong/rusak ({type(e).__name__}). Data MUNGKIN SUDAH tersimpan "
                    "untuk permintaan yang menulis - cek di aplikasi SiYuan, jangan ulangi begitu saja.",
                    KELUAR_TIDAK_PASTI, mungkin_terkirim=True) from e
    except (urllib.error.URLError, OSError) as e:
        alasan = getattr(e, "reason", e)
        if isinstance(alasan, ConnectionRefusedError) or "refused" in str(alasan).lower():
            raise Gagal(
                "Tidak bisa terhubung ke kernel SiYuan. Pastikan aplikasi SiYuan sedang berjalan "
                f"(alamat {url_dasar}). Buka aplikasi SiYuan dulu, tunggu sampai siap, lalu coba lagi.",
                KELUAR_KONEKSI,
            ) from e
        raise Gagal(f"Koneksi ke kernel SiYuan terputus/timeout ({alasan}).", KELUAR_TIDAK_PASTI,
                    mungkin_terkirim=True) from e
    try:
        j = json.loads(mentah.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise Gagal("Jawaban kernel SiYuan bukan JSON yang valid (mungkin terpotong).", KELUAR_TIDAK_PASTI,
                    mungkin_terkirim=True) from e
    if j.get("code", 0) != 0:
        raise Gagal(f"Kernel SiYuan: {j.get('msg') or 'galat tanpa pesan'} (code {j.get('code')}).", KELUAR_LAIN)
    return j.get("data")


# ------------------------------------------------------------------ template SQL tetap (whitelist)
SQL_CARI = (
    "SELECT root_id, box, hpath, content, type, updated FROM blocks "
    "WHERE type IN ('d','h','p') AND (content LIKE '%{k}%' ESCAPE '\\' OR hpath LIKE '%{k}%' ESCAPE '\\') "
    "ORDER BY updated DESC LIMIT {batas}"
)
SQL_LAMA = (
    "SELECT id, box, hpath, updated FROM blocks WHERE type='d' AND updated < '{cutoff}'{filt} "
    "ORDER BY updated ASC LIMIT 200"
)
SQL_DAFTAR_DOKUMEN_BUKU = "SELECT id, hpath, updated FROM blocks WHERE type='d' AND box='{box}' ORDER BY hpath LIMIT 2000"


def escape_like(nilai):
    """Escape literal SQLite DULU, lalu escape wildcard LIKE (%, _) dengan backslash agar
    dicari sebagai teks apa adanya (dipasangkan dengan klausa ESCAPE '\\' di template)."""
    nilai = escape_sql_literal(nilai)
    return nilai.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def jalankan_sql(url, token, lokal, stmt):
    return panggil(url, token, "/api/query/sql", {"stmt": stmt}, lokal) or []


# ------------------------------------------------------------------ perintah
def p_cek(url, token, lokal, izinkan_jarak_jauh):
    buku = panggil(url, token, "/api/notebook/lsNotebooks", {}, lokal).get("notebooks", [])
    baris = [f"OK - kernel SiYuan bisa dihubungi ({url})", f"Token API: valid ({samarkan_token(token)})",
             f"Buku catatan: {len(buku)}"]
    for b in buku:
        baris.append(f"  - {b['name']} (id {b['id']}){' [tertutup]' if b.get('closed') else ''}")
    if not izinkan_jarak_jauh:
        baris.append("Alamat: localhost saja (default aman).")
    return {"teks": "\n".join(baris), "buku_catatan": buku}


def p_daftar_buku(url, token, lokal):
    buku = panggil(url, token, "/api/notebook/lsNotebooks", {}, lokal).get("notebooks", [])
    if not buku:
        return {"teks": "Belum ada buku catatan di SiYuan.", "buku_catatan": []}
    baris = ["BUKU CATATAN SIYUAN"] + [
        f"- {b['name']} (id {b['id']}){' [tertutup]' if b.get('closed') else ''}" for b in buku
    ]
    return {"teks": "\n".join(baris), "buku_catatan": buku}


def p_cari(url, token, lokal, kata, maks):
    if not kata or not kata.strip():
        raise Gagal("Kata kunci pencarian tidak boleh kosong.", KELUAR_ARG)
    k = escape_like(kata)
    baris_sql = jalankan_sql(url, token, lokal, SQL_CARI.format(k=k, batas=int(maks)))
    dilihat, hasil = set(), []
    for r in baris_sql:
        rid = r.get("root_id")
        if rid in dilihat:
            continue
        dilihat.add(rid)
        hasil.append({"id": rid, "box": r.get("box"), "judul": (r.get("hpath") or "").rsplit("/", 1)[-1] or "(?)",
                      "path": r.get("hpath"), "cuplikan": potong_cuplikan(r.get("content"), kata)})
    if not hasil:
        return {"teks": f"Tidak ada dokumen yang cocok dengan '{kata}'.", "hasil": []}
    baris = [f"HASIL PENCARIAN '{kata}' ({len(hasil)} dokumen)"]
    for h in hasil:
        baris.append(f"- {h['judul']}  [{h['path']}]  (id {h['id']})\n    ...{h['cuplikan']}...")
    baris.append("Cuplikan bisa terpotong. Untuk menjawab pertanyaan isi, jalankan `baca --id <id>` pada dokumen "
                 "yang cocok dan jawab dari isi lengkapnya.")
    return {"teks": "\n".join(baris), "hasil": hasil}


def p_baca(url, token, lokal, doc_id, notebook, path):
    if not doc_id:
        if not (notebook and path):
            raise Gagal("Isi --id, atau --notebook dan --path bersamaan.", KELUAR_ARG)
        ids = panggil(url, token, "/api/filetree/getIDsByHPath", {"notebook": notebook, "path": path}, lokal)
        if not ids:
            raise Gagal(f"Tidak ada dokumen di path '{path}' pada buku catatan itu.", KELUAR_LAIN)
        doc_id = ids[0]
    data = panggil(url, token, "/api/export/exportMdContent", {"id": doc_id}, lokal)
    if not isinstance(data, dict):
        raise Gagal(f"Dokumen dengan id '{doc_id}' tidak ditemukan.", KELUAR_LAIN)
    return {"teks": f"# {data.get('hPath')}\n\n{data.get('content', '')}", "id": doc_id,
            "path": data.get("hPath"), "markdown": data.get("content", "")}


def _ringkas_isi(md):
    baris = [b for b in str(md or "").splitlines() if b.strip()]
    return len(baris), len(str(md or ""))


def _slug(path):
    t = re.sub(r"[^A-Za-z0-9]+", "-", path).strip("-")
    return (t or "dokumen")[:60]


def p_buat(url, token, lokal, notebook, path, markdown, ya, timpa, konfirmasi_timpa=False, folder_cadangan=None):
    if not notebook or not path:
        raise Gagal("Isi --notebook dan --path.", KELUAR_ARG)
    if not path.startswith("/"):
        raise Gagal("--path harus diawali '/' (mis. /SOP/Buka Toko).", KELUAR_ARG)
    ada = panggil(url, token, "/api/filetree/getIDsByHPath", {"notebook": notebook, "path": path}, lokal)
    if ada and not timpa:
        raise Gagal(
            f"TIDAK DIBUAT: sudah ada dokumen di path '{path}' (id {ada[0]}). Pakai perintah `tambah` untuk "
            "menambahkan isi tanpa menghapus yang lama, atau `buat ... --timpa` untuk MENGGANTI seluruh isi "
            "(wajib pratinjau + konfirmasi akhir + cadangan).",
            KELUAR_DOBEL,
        )
    pratinjau = {
        "notebook": notebook, "path": path, "aksi": "GANTI (dokumen lama akan DIHAPUS)" if (ada and timpa) else "BARU",
        "panjang_markdown": len(markdown), "cuplikan": markdown.strip()[:300],
    }
    lama_md = None
    if ada and timpa:
        data = panggil(url, token, "/api/export/exportMdContent", {"id": ada[0]}, lokal)
        lama_md = data.get("content", "") if isinstance(data, dict) else ""
        b_lama, k_lama = _ringkas_isi(lama_md)
        b_baru, k_baru = _ringkas_isi(markdown)
        pratinjau.update({"judul": path.rsplit("/", 1)[-1], "baris_lama": b_lama, "baris_baru": b_baru,
                          "baris_hilang": max(0, b_lama - b_baru)})
    if not ya:
        teks = (
            f"PRATINJAU BUAT DOKUMEN\nBuku catatan: {notebook}\nPath: {path}\n"
            f"Aksi: {pratinjau['aksi']}\n"
        )
        if lama_md is not None:
            teks += (
                f"Judul dokumen: {pratinjau['judul']}\n"
                f"ISI LAMA: {b_lama} baris berisi, {k_lama} karakter. ISI BARU: {b_baru} baris berisi, {k_baru} karakter. "
                f"Baris yang hilang bila ditimpa: {pratinjau['baris_hilang']} (selisih; seluruh isi lama diganti).\n"
                f"Cuplikan isi lama:\n---\n{lama_md.strip()[:500]}\n---\n"
            )
        teks += f"Isi baru ({len(markdown)} karakter):\n---\n{markdown.strip()[:500]}\n---\n"
        if lama_md is not None:
            teks += ("Tampilkan pratinjau ini ke pengguna dan minta konfirmasi akhir yang eksplisit "
                     "(mis. 'Ketik TIMPA untuk melanjutkan'). Setelah itu jalankan ulang dengan "
                     f"--timpa --ya --konfirmasi-timpa. Cadangan isi lama otomatis disimpan ke folder {_folder_cadangan(folder_cadangan)} "
                     "(di luar folder skill).")
        else:
            teks += "Simpan ke SiYuan? Jalankan ulang dengan --ya."
        return {"teks": teks, "pratinjau": pratinjau, "disimpan": False}
    if ada and timpa and not konfirmasi_timpa:
        raise Gagal(
            "TIDAK DITIMPA: menimpa wajib pratinjau dan konfirmasi akhir eksplisit dari pengguna. Jalankan dulu "
            "tanpa --ya untuk pratinjau, tunjukkan ke pengguna, lalu setelah pengguna mengonfirmasi tegas "
            "jalankan dengan --timpa --ya --konfirmasi-timpa.", KELUAR_ARG)
    try:
        panggil(url, token, "/api/notebook/openNotebook", {"notebook": notebook}, lokal)
    except Gagal:
        pass  # notebook mungkin sudah terbuka / tidak kritis untuk lanjut
    berkas_cadangan = None
    if ada and timpa:
        folder = _folder_cadangan(folder_cadangan)
        os.makedirs(folder, exist_ok=True)
        berkas_cadangan = os.path.join(folder, f"{_slug(path)}-sebelum-{dt.datetime.now():%Y-%m-%d-%H%M%S}.md")
        with open(berkas_cadangan, "w", encoding="utf-8") as f:
            f.write(lama_md)
        panggil(url, token, "/api/filetree/removeDocByID", {"id": ada[0]}, lokal)
        try:
            doc_id = panggil(url, token, "/api/filetree/createDocWithMd",
                             {"notebook": notebook, "path": path, "markdown": markdown}, lokal)
        except Gagal as g:
            try:  # pulihkan isi lama dari cadangan
                panggil(url, token, "/api/filetree/createDocWithMd",
                        {"notebook": notebook, "path": path, "markdown": lama_md}, lokal)
                pulih = "Dokumen lama sudah dipulihkan dari cadangan."
            except Gagal:
                pulih = "Pemulihan otomatis GAGAL; pulihkan manual dari berkas cadangan."
            raise Gagal(f"Pembuatan dokumen baru gagal ({g.pesan}). {pulih} Cadangan: {berkas_cadangan}",
                        KELUAR_TIDAK_PASTI, mungkin_terkirim=True) from g
        return {"teks": f"TERSIMPAN: dokumen '{path}' DITIMPA (id {doc_id}). Cadangan isi lama: {berkas_cadangan} "
                         "(path lengkap, di luar folder skill - sebutkan path ini ke pengguna)",
                "id": doc_id, "disimpan": True, "cadangan": berkas_cadangan}
    doc_id = panggil(url, token, "/api/filetree/createDocWithMd", {"notebook": notebook, "path": path,
                                                                     "markdown": markdown}, lokal)
    return {"teks": f"TERSIMPAN: dokumen '{path}' dibuat di SiYuan (id {doc_id}).", "id": doc_id, "disimpan": True}


def p_tambah(url, token, lokal, doc_id, markdown, ya):
    if not doc_id:
        raise Gagal("Isi --id (id dokumen/blok tujuan).", KELUAR_ARG)
    if not ya:
        teks = (f"PRATINJAU TAMBAH ISI\nTujuan (id): {doc_id}\nIsi baru ({len(markdown)} karakter):\n---\n"
                f"{markdown.strip()[:500]}\n---\nIsi LAMA tidak dihapus, hanya ditambahkan di akhir. "
                "Lanjutkan? Jalankan ulang dengan --ya.")
        return {"teks": teks, "disimpan": False}
    hasil = panggil(url, token, "/api/block/appendBlock", {"data": markdown, "dataType": "markdown",
                                                            "parentID": doc_id}, lokal)
    return {"teks": f"TERSIMPAN: isi ditambahkan ke dokumen/blok {doc_id}.", "disimpan": True, "hasil": hasil}


def p_lama(url, token, lokal, hari, notebook):
    if hari <= 0:
        raise Gagal("--hari harus lebih dari 0.", KELUAR_ARG)
    cutoff = (dt.datetime.now() - dt.timedelta(days=hari)).strftime("%Y%m%d%H%M%S")
    assert re.match(r"^\d{14}$", cutoff)
    filt = f" AND box='{escape_sql_literal(notebook)}'" if notebook else ""
    baris = jalankan_sql(url, token, lokal, SQL_LAMA.format(cutoff=cutoff, filt=filt))
    if not baris:
        return {"teks": f"Tidak ada dokumen yang belum diperbarui > {hari} hari.", "dokumen": []}
    out = [f"DOKUMEN BELUM DIPERBARUI > {hari} HARI ({len(baris)} dokumen)"]
    for b in baris:
        out.append(f"- {b.get('hpath')}  (terakhir: {b.get('updated')})")
    return {"teks": "\n".join(out), "dokumen": baris}


def _kosong(teks):
    """True bila isi dokumen kosong atau hanya berisi placeholder tak kasatmata (dokumen induk
    otomatis yang dibuat SiYuan untuk path bertingkat, mis. saat membuat '/FAQ/Jam Buka' otomatis
    membuat dokumen kosong '/FAQ' berisi frontmatter + judul otomatis + satu karakter tak kasatmata)."""
    t = str(teks or "")
    t = re.sub(r"^---.*?---", "", t, count=1, flags=re.DOTALL)  # buang frontmatter YAML di awal
    t = re.sub(r"^\s*#+[^\n]*\n?", "", t, count=1)  # buang satu baris judul markdown di awal (mis. '# FAQ')
    t = re.sub(r"[\s​‌‍﻿]", "", t)  # buang spasi & karakter tak kasatmata
    return t == ""


def p_ekspor_basis(url, token, lokal, notebook, file_tujuan, filter_kata):
    if not notebook:
        raise Gagal("Isi --notebook.", KELUAR_ARG)
    baris = jalankan_sql(url, token, lokal, SQL_DAFTAR_DOKUMEN_BUKU.format(box=escape_sql_literal(notebook)))
    if filter_kata:
        fk = filter_kata.lower()
        baris = [b for b in baris if fk in (b.get("hpath") or "").lower()]
    if not baris:
        return {"teks": "Tidak ada dokumen untuk diekspor (cek --notebook / --filter).", "jumlah": 0}
    potongan = [f"<!-- Basis pengetahuan diekspor dari SiYuan pada {dt.datetime.now():%Y-%m-%d %H:%M} -->\n"]
    jumlah = 0
    for b in sorted(baris, key=lambda x: x.get("hpath") or ""):
        data = panggil(url, token, "/api/export/exportMdContent", {"id": b["id"]}, lokal)
        isi = data.get("content", "")
        if _kosong(isi):
            continue  # lewati dokumen induk otomatis yang kosong (path bertingkat), bukan isi asli
        jumlah += 1
        potongan.append(f"\n\n---\n\n# {data.get('hPath')}\n\n{isi}")
    if jumlah == 0:
        return {"teks": "Tidak ada dokumen berisi (semua kosong) untuk diekspor.", "jumlah": 0}
    gabungan = "".join(potongan)
    tujuan = file_tujuan or "basis-pengetahuan.md"
    with open(tujuan, "w", encoding="utf-8") as f:
        f.write(gabungan)
    return {"teks": f"TERSIMPAN: {jumlah} dokumen digabung ke '{tujuan}' ({len(gabungan)} karakter).",
            "jumlah": jumlah, "file": tujuan}


# ------------------------------------------------------------------ CLI
def buat_parser():
    ap = argparse.ArgumentParser(prog="siyuan.py", description="Asisten SiYuan lokal (Komunitech)", allow_abbrev=False)
    ap.add_argument("--url", default=os.environ.get("SIYUAN_URL", URL_DEFAULT))
    ap.add_argument("--kunci-file")
    ap.add_argument("--izinkan-jarak-jauh", action="store_true")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="perintah", required=True)

    sub.add_parser("cek", allow_abbrev=False)
    sp = sub.add_parser("simpan-kunci", allow_abbrev=False)
    sp.add_argument("--ya", action="store_true")
    sp.add_argument("--token")  # untuk pengujian otomatis saja; interaktif dianjurkan di pemakaian nyata

    sub.add_parser("daftar-buku", allow_abbrev=False)

    sc = sub.add_parser("cari", allow_abbrev=False)
    sc.add_argument("kata")
    sc.add_argument("--maks", type=int, default=20)

    sb = sub.add_parser("baca", allow_abbrev=False)
    sb.add_argument("--id")
    sb.add_argument("--notebook")
    sb.add_argument("--path")

    sm = sub.add_parser("buat", allow_abbrev=False)
    sm.add_argument("--notebook", required=True)
    sm.add_argument("--path", required=True)
    sm.add_argument("--md")
    sm.add_argument("--md-file")
    sm.add_argument("--stdin", action="store_true", help="baca Markdown dari input standar")
    sm.add_argument("--ya", action="store_true")
    sm.add_argument("--timpa", action="store_true")
    sm.add_argument("--konfirmasi-timpa", action="store_true",
                    help="hanya setelah pengguna mengonfirmasi tegas pratinjau penimpaan")
    sm.add_argument("--cadangan-dir", help="folder cadangan isi lama (default: ~/KomunitechData/siyuan/cadangan, di luar folder skill; "
                         "ENV KOMUNITECH_SIYUAN_CADANGAN atau KOMUNITECH_DATA)")

    st = sub.add_parser("tambah", allow_abbrev=False)
    st.add_argument("--id", required=True)
    st.add_argument("--md")
    st.add_argument("--md-file")
    st.add_argument("--stdin", action="store_true")
    st.add_argument("--ya", action="store_true")

    sl = sub.add_parser("lama", allow_abbrev=False)
    sl.add_argument("--hari", type=int, default=90)
    sl.add_argument("--notebook")

    se = sub.add_parser("ekspor-basis", allow_abbrev=False)
    se.add_argument("--notebook", required=True)
    se.add_argument("--file")
    se.add_argument("--filter")
    return ap


def main(argv=None):
    ap = buat_parser()
    args = ap.parse_args(argv)
    try:
        if args.perintah == "simpan-kunci":
            if args.token:
                cetak("PERINGATAN: token lewat argumen --token terlihat di riwayat perintah & daftar proses. "
                      "Pakai tanpa --token (diketik interaktif) untuk pemakaian nyata.")
            token = args.token or input("Tempel token API SiYuan lalu Enter (tidak akan tampil di log): ").strip()
            if not token:
                raise Gagal("Token tidak boleh kosong.", KELUAR_ARG)
            path = args.kunci_file or FILE_KUNCI_DEFAULT
            simpan_kunci_ke_file(path, token, args.ya)
            cetak(f"Tersimpan di {path} (izin 600). Jangan bagikan file ini ke siapa pun.")
            return 0

        lokal = periksa_alamat(args.url, args.izinkan_jarak_jauh)
        token = ambil_token(args)

        if args.perintah == "cek":
            hasil = p_cek(args.url, token, lokal, args.izinkan_jarak_jauh)
        elif args.perintah == "daftar-buku":
            hasil = p_daftar_buku(args.url, token, lokal)
        elif args.perintah == "cari":
            hasil = p_cari(args.url, token, lokal, args.kata, args.maks)
        elif args.perintah == "baca":
            hasil = p_baca(args.url, token, lokal, args.id, args.notebook, args.path)
        elif args.perintah == "buat":
            markdown = baca_teks_masukan(args.md, args.md_file, args.stdin)
            hasil = p_buat(args.url, token, lokal, args.notebook, args.path, markdown, args.ya, args.timpa,
                            args.konfirmasi_timpa, args.cadangan_dir)
        elif args.perintah == "tambah":
            markdown = baca_teks_masukan(args.md, args.md_file, args.stdin)
            hasil = p_tambah(args.url, token, lokal, args.id, markdown, args.ya)
        elif args.perintah == "lama":
            hasil = p_lama(args.url, token, lokal, args.hari, args.notebook)
        elif args.perintah == "ekspor-basis":
            hasil = p_ekspor_basis(args.url, token, lokal, args.notebook, args.file, args.filter)
        else:
            raise Gagal(f"Perintah tidak dikenal: {args.perintah}", KELUAR_ARG)
    except Gagal as g:
        if args.json:
            cetak(json.dumps({"galat": g.pesan, "kode": g.kode, "mungkin_terkirim": g.mungkin_terkirim},
                              ensure_ascii=False))
        else:
            cetak("GAGAL: " + g.pesan)
            if g.saran:
                cetak("Saran: " + g.saran)
        return g.kode
    except KeyboardInterrupt:
        cetak("Dibatalkan.")
        return KELUAR_ARG

    if args.json:
        cetak(json.dumps(hasil, ensure_ascii=False, default=str))
    else:
        cetak(hasil.get("teks", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
