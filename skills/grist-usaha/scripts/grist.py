#!/usr/bin/env python3
"""grist-usaha (Komunitech) - bantu merancang, mengisi, dan membaca dokumen Grist milik
pengguna yang terpasang di komputernya sendiri (lihat docs/panduan-grist.md).

Dua cara kerja, TIDAK saling bergantung:

1. **Baca file .grist langsung (read-only, SELALU tersedia, tanpa API/Grist perlu menyala)**
   File `.grist` adalah file SQLite biasa. Perintah `daftar-tabel`, `ringkasan`, `ekspor-csv`
   membukanya dengan mode BACA SAJA (`sqlite3` standar Python, tanpa paket tambahan) - tidak
   pernah menulis apa pun ke file itu.

2. **REST API grist-core lokal (opsional, HANYA bila Docker/grist-core sedang menyala dan
   pengguna sudah menyimpan kunci API - lihat panduan bagian 6)**. Dipakai perintah `cek`,
   `buat-tabel`, `impor-csv`. Alamat default `http://localhost:8484`. Kunci dikirim lewat
   header `Authorization: Bearer <kunci>` sesuai API resmi Grist.

Keamanan kunci API:
  ENV GRIST_URL             (default: http://localhost:8484)
  ENV GRIST_API_KEY         (opsional, dipakai bila --kunci-file tidak diberikan)
  ENV GRIST_API_KEY_FILE    (opsional, path file kunci pengganti default)
  ENV GRIST_ALLOW_REMOTE=1  (WAJIB diisi bila GRIST_URL bukan localhost/127.0.0.1 - penegasan
                              eksplisit bahwa pengguna sadar data akan dikirim ke alamat itu)
Kunci TIDAK PERNAH dicetak utuh ke layar/log; hanya 4 karakter terakhir yang ditampilkan.

Contoh:
  python3 grist.py cek
  python3 grist.py simpan-kunci
  python3 grist.py pola daftar
  python3 grist.py pola tampilkan pelanggan
  python3 grist.py buat-tabel pesanan --dokumen "Data Usaha Saya"
  python3 grist.py bersihkan-csv daftar-pelanggan.csv
  python3 grist.py impor-csv daftar-pelanggan-bersih.csv --dokumen "Data Usaha Saya" --tabel Pelanggan
  python3 grist.py daftar-tabel "Data Usaha Saya.grist"
  python3 grist.py ringkasan "Data Usaha Saya.grist" Pelanggan
  python3 grist.py ekspor-csv "Data Usaha Saya.grist" Pelanggan --keluaran pelanggan.csv

Referensi endpoint & format: `research/sources/grist-2026-09-26.md` (dikonfirmasi langsung
dari kode sumber resmi `grist-core` v1.7.19 - app/server/lib/DocApi.ts, app/gen-server/ApiServer.ts,
app/server/lib/DocStorage.ts, sandbox/grist/schema.py). Endpoint REST **belum** diuji terhadap
server Grist yang sungguhan menyala (lihat catatan kejujuran di README.md skill ini); baca .grist
lewat SQLite sudah diuji dengan file contoh yang skemanya sama persis dengan schema.py resmi.
"""
import argparse
import csv
import getpass
import json
import os
import re
import sqlite3
import stat
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal
from pathlib import Path

VERSI = "1.0.2"
APLIKASI = "grist-usaha"
LOKAL_DIIZINKAN = {"localhost", "127.0.0.1", "::1"}
FILE_KUNCI_DEFAULT = Path.home() / ".komunitech" / "grist-kunci.txt"
POLA_LAN = re.compile(r"^(192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.)")


class Gagal(Exception):
    """Error yang pesannya aman & jelas untuk ditampilkan ke pengguna awam."""

    def __init__(self, pesan, kode=1):
        super().__init__(pesan)
        self.kode = kode


# ---------------------------------------------------------------------------
# Pola tabel siap pakai (lihat references/pola-tabel-umkm.md untuk penjelasan awam)
# ---------------------------------------------------------------------------
# Tipe kolom di sini adalah tipe Grist asli (dipakai langsung sebagai field "type" saat
# memanggil REST API POST /tables dan POST /columns).
POLA_TABEL = {
    "pelanggan": {
        "tabel_default": "Pelanggan",
        "judul": "Daftar Pelanggan",
        "kolom": [
            ("Nama", "Nama", "Text"),
            ("Telepon", "No. WA/Telepon", "Text"),
            ("Kota", "Kota", "Text"),
            ("Sumber", "Sumber", "Text"),
            ("Catatan", "Catatan", "Text"),
            ("TanggalDaftar", "Tgl Daftar", "Date"),
        ],
        "rumus": {"TeleponRapi": "rumus_wa_rapi (references/rumus-umum.md #1)"},
    },
    "pesanan": {
        "tabel_default": "Pesanan",
        "judul": "Pesanan",
        "kolom": [
            ("Tanggal", "Tanggal", "Date"),
            ("Pelanggan", "Pelanggan", "Text"),
            ("Barang", "Barang", "Text"),
            ("Jumlah", "Jumlah", "Int"),
            ("HargaSatuan", "Harga Satuan", "Numeric"),
            ("Diskon", "Diskon %", "Numeric"),
            ("Status", "Status", "Text"),
            ("Catatan", "Catatan", "Text"),
        ],
        "rumus": {"Total": "rumus_total_baris (references/rumus-umum.md #2)"},
    },
    "stok": {
        "tabel_default": "Stok",
        "judul": "Stok Sederhana",
        "kolom": [
            ("Nama", "Nama Barang", "Text"),
            ("Kode", "Kode/SKU", "Text"),
            ("Satuan", "Satuan", "Text"),
            ("StokMasuk", "Masuk", "Int"),
            ("StokKeluar", "Keluar", "Int"),
            ("BatasMinimum", "Batas Minimum", "Int"),
        ],
        "rumus": {
            "StokSaatIni": "rumus_sisa_stok (references/rumus-umum.md #3)",
            "Status": "rumus_status_stok (references/rumus-umum.md #4)",
        },
    },
    "jadwal-konten": {
        "tabel_default": "JadwalKonten",
        "judul": "Jadwal Konten",
        "kolom": [
            ("Tanggal", "Tanggal Tayang", "Date"),
            ("Platform", "Platform", "Text"),
            ("Judul", "Judul/Topik", "Text"),
            ("Draf", "Draf Isi", "Text"),
            ("StatusProduksi", "Status", "Text"),
            ("PJ", "Penanggung Jawab", "Text"),
        ],
        "rumus": {"HariMenuju": "rumus_hari_menuju (references/rumus-umum.md #5)"},
    },
}


# ---------------------------------------------------------------------------
# Konfigurasi & keamanan alamat server + kunci API
# ---------------------------------------------------------------------------

def ambil_base_url(arg_url=None):
    url = (arg_url or os.environ.get("GRIST_URL") or "http://localhost:8484").rstrip("/")
    host = urllib.parse.urlparse(url).hostname or ""
    if host in LOKAL_DIIZINKAN:
        return url
    if os.environ.get("GRIST_ALLOW_REMOTE") != "1":
        raise Gagal(
            f"Alamat Grist ({url}) bukan localhost/127.0.0.1. Skill ini dirancang untuk komputer "
            "sendiri. Jika kamu memang sengaja memakai server lain dan paham risikonya (data "
            "dikirim ke alamat itu), set environment variable GRIST_ALLOW_REMOTE=1 lalu coba lagi.",
            kode=2,
        )
    if not POLA_LAN.match(host) and not url.startswith("https://"):
        raise Gagal(
            f"Alamat Grist ({url}) tampak berada di internet (bukan jaringan lokal 192.168.x/10.x/"
            "172.16-31.x), jadi WAJIB memakai https:// agar kunci API tidak bocor di jalan. "
            "Ubah URL ke https://... atau pastikan itu benar alamat jaringan lokal.",
            kode=2,
        )
    return url


def _cek_izin_file(path):
    mode = path.stat().st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise Gagal(
            f"File kunci {path} bisa dibaca pengguna lain (izin terlalu longgar). Jalankan "
            f"'chmod 600 {path}' lalu coba lagi.",
            kode=5,
        )


def ambil_kunci(arg_kunci_file=None):
    if arg_kunci_file:
        p = Path(arg_kunci_file).expanduser()
        if not p.is_file() or not p.read_text(encoding="utf-8").strip():
            raise Gagal(f"File kunci '{p}' (dari --kunci-file) tidak ditemukan/kosong.", kode=5)
        _cek_izin_file(p)
        if os.environ.get("GRIST_API_KEY"):
            print("PERINGATAN: --kunci-file dipakai; ENV GRIST_API_KEY DIABAIKAN.", file=sys.stderr)
        return p.read_text(encoding="utf-8").strip()
    if os.environ.get("GRIST_API_KEY"):
        return os.environ["GRIST_API_KEY"].strip()
    p = Path(os.environ.get("GRIST_API_KEY_FILE") or FILE_KUNCI_DEFAULT).expanduser()
    if not p.is_file() or not p.read_text(encoding="utf-8").strip():
        raise Gagal(
            f"Belum ada kunci API tersimpan ({p}). Jalankan 'python3 grist.py simpan-kunci' dulu "
            "(lihat docs/panduan-grist.md bagian 6). REST API bersifat OPSIONAL - kamu tetap bisa "
            "memakai 'daftar-tabel'/'ringkasan'/'ekspor-csv' langsung ke file .grist tanpa ini.",
            kode=5,
        )
    _cek_izin_file(p)
    kunci = p.read_text(encoding="utf-8").strip()
    if re.search(r"\s", kunci):
        raise Gagal(f"Kunci API di {p} berisi spasi/baris baru - kemungkinan tersalin rusak. "
                    "Salin ulang dari Grist (Profile Settings > API Key) dan jalankan simpan-kunci lagi.", kode=5)
    return kunci


def masker(kunci):
    return ("*" * max(len(kunci) - 4, 0)) + kunci[-4:] if kunci else "(kosong)"


def cmd_simpan_kunci(args):
    tujuan = Path(args.kunci_file).expanduser() if args.kunci_file else FILE_KUNCI_DEFAULT
    print(f"Kunci akan disimpan di: {tujuan}")
    if tujuan.is_file() and not args.ya:
        raise Gagal(
            f"File kunci '{tujuan}' sudah ada. Tambahkan --ya untuk menimpa (mengganti kunci "
            "lama), atau pakai --kunci-file lain untuk menyimpan sebagai kunci kedua.",
            kode=2,
        )
    kunci = getpass.getpass("Tempel kunci API Grist (tidak akan terlihat), lalu Enter: ").strip()
    if not kunci:
        raise Gagal("Kunci kosong, tidak disimpan.", kode=2)
    if re.search(r"\s", kunci):
        raise Gagal("Kunci mengandung spasi/baris baru - kemungkinan tersalin tidak lengkap. Ulangi salin dari Grist.", kode=2)
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    tujuan.write_text(kunci + "\n", encoding="utf-8")
    os.chmod(tujuan, 0o600)
    print(f"Tersimpan ({masker(kunci)}), izin file diatur 600 (hanya kamu yang bisa baca).")
    return 0


# ---------------------------------------------------------------------------
# Panggilan REST API Grist (opsional)
# ---------------------------------------------------------------------------

def panggil_grist(base_url, kunci, path, method="GET", body=None, timeout=30):
    """Kembalikan objek JSON yang sudah di-parse. Melempar Gagal dengan pesan ramah."""
    url = base_url + path
    headers = {"Authorization": f"Bearer {kunci}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            mentah = resp.read()
    except urllib.error.HTTPError as e:
        mentah = e.read()
        pesan = None
        try:
            j = json.loads(mentah.decode("utf-8", errors="replace"))
            pesan = j.get("error") if isinstance(j, dict) else None
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        if e.code == 401:
            raise Gagal("401 tidak sah - kunci API salah/diganti/dihapus. Buat kunci baru di Grist "
                        "(Profile Settings) lalu 'simpan-kunci' lagi.", kode=5) from None
        if e.code == 403:
            raise Gagal(f"403 tidak diizinkan{f' ({pesan})' if pesan else ''} - kunci ini tidak "
                        "punya akses ke dokumen itu.", kode=5) from None
        if e.code == 404:
            raise Gagal(f"404 tidak ditemukan - dokumen/tabel/alamat salah{f': {pesan}' if pesan else ''}.", kode=2) from None
        raise Gagal(f"Grist membalas galat {e.code}{f': {pesan}' if pesan else ''}.", kode=6) from None
    except urllib.error.URLError as e:
        raise Gagal(f"Tidak bisa menghubungi Grist di {base_url} ({e.reason}). Pastikan Grist "
                    "sedang menyala (docs/panduan-grist.md bagian 3.3).", kode=3) from None
    try:
        return json.loads(mentah.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise Gagal("Jawaban Grist tidak bisa dibaca (bukan JSON) - kemungkinan alamat GRIST_URL salah.", kode=6) from None


def _daftar_dokumen(base_url, kunci):
    """Kembalikan list (docId, namaDok, namaWorkspace, domainOrg)."""
    hasil = []
    orgs = panggil_grist(base_url, kunci, "/api/orgs")
    for org in orgs:
        oid = org.get("id")
        try:
            wss = panggil_grist(base_url, kunci, f"/api/orgs/{oid}/workspaces")
        except Gagal:
            continue
        for ws in wss:
            for doc in ws.get("docs", []) or []:
                hasil.append((doc.get("id"), doc.get("name"), ws.get("name"), org.get("domain") or org.get("name")))
    return hasil


def cari_dokumen(base_url, kunci, sebutan):
    """Terima docId langsung, atau nama dokumen (dicocokkan tanpa peduli besar/kecil huruf).
    Kembalikan docId tunggal atau melempar Gagal (tidak ketemu / lebih dari satu cocok)."""
    semua = _daftar_dokumen(base_url, kunci)
    persis_id = [d for d in semua if d[0] == sebutan]
    if len(persis_id) == 1:
        return persis_id[0][0]
    cocok = [d for d in semua if sebutan.strip().lower() in (d[1] or "").lower()]
    if len(cocok) == 1:
        return cocok[0][0]
    if not cocok:
        daftar = "\n".join(f"  - {n} (workspace: {w}, org: {o})" for _, n, w, o in semua) or "  (tidak ada dokumen yang bisa diakses kunci ini)"
        raise Gagal(f"Dokumen '{sebutan}' tidak ditemukan. Dokumen yang bisa diakses kunci ini:\n{daftar}", kode=2)
    daftar = "\n".join(f"  - {n} (docId: {i}, workspace: {w})" for i, n, w, _ in cocok)
    raise Gagal(f"Ada {len(cocok)} dokumen bernama mirip '{sebutan}'. Sebutkan salah satu docId ini:\n{daftar}", kode=2)


def cmd_cek(args):
    base_url = ambil_base_url(args.url)
    try:
        kunci = ambil_kunci(args.kunci_file)
    except Gagal as e:
        print(f"CEK GRIST — {APLIKASI} v{VERSI}")
        print(f"Alamat: {base_url}")
        print(f"Kunci API: belum ada ({e})")
        print("Ini WAJAR bila kamu belum memakai REST API. Perintah 'daftar-tabel'/'ringkasan'/")
        print("'ekspor-csv' tetap jalan langsung ke file .grist tanpa kunci ini.")
        return 0
    dokumen = _daftar_dokumen(base_url, kunci)
    print(f"CEK GRIST — {APLIKASI} v{VERSI}")
    print(f"Alamat: {base_url}")
    print(f"Kunci API: {masker(kunci)}")
    if not dokumen:
        print("Terhubung, tapi kunci ini belum bisa mengakses dokumen mana pun.")
    else:
        print(f"Dokumen yang bisa diakses ({len(dokumen)}):")
        for doc_id, nama, ws, org in dokumen:
            print(f"  - {nama}  (docId: {doc_id}, workspace: {ws}, org: {org})")
    if args.json:
        print(json.dumps({"alamat": base_url, "kunci": masker(kunci), "dokumen": [
            {"id": i, "nama": n, "workspace": w, "org": o} for i, n, w, o in dokumen
        ]}, ensure_ascii=False, indent=2))
    return 0


# ---------------------------------------------------------------------------
# pola daftar / pola tampilkan
# ---------------------------------------------------------------------------

def cmd_pola_daftar(args):
    print("Pola tabel siap pakai (lihat references/pola-tabel-umkm.md untuk penjelasan lengkap):")
    for kunci, p in POLA_TABEL.items():
        print(f"  - {kunci:14s} {p['judul']} ({len(p['kolom'])} kolom + {len(p['rumus'])} rumus)")
    return 0


def cmd_pola_tampilkan(args):
    p = POLA_TABEL.get(args.nama)
    if not p:
        raise Gagal(f"Pola '{args.nama}' tidak dikenal. Pilihan: {', '.join(POLA_TABEL)}", kode=2)
    print(f"POLA: {p['judul']}  (nama tabel default: {p['tabel_default']})")
    print("Kolom biasa:")
    for col_id, label, tipe in p["kolom"]:
        print(f"  - {col_id:16s} [{tipe:8s}] label: {label}")
    if p["rumus"]:
        print("Kolom rumus (tempel rumusnya dari references/rumus-umum.md):")
        for col_id, ket in p["rumus"].items():
            print(f"  - {col_id:16s} -> {ket}")
    return 0


def cmd_buat_tabel(args):
    p = POLA_TABEL.get(args.pola)
    if not p:
        raise Gagal(f"Pola '{args.pola}' tidak dikenal. Pilihan: {', '.join(POLA_TABEL)}", kode=2)
    nama_tabel = args.tabel or p["tabel_default"]
    if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", nama_tabel):
        raise Gagal("Nama tabel harus diawali huruf, hanya huruf/angka/garis bawah (aturan Grist).", kode=2)
    base_url = ambil_base_url(args.url)
    kunci = ambil_kunci(args.kunci_file)
    doc_id = cari_dokumen(base_url, kunci, args.dokumen)

    kolom_req = [{"id": col_id, "fields": {"label": label, "type": tipe}} for col_id, label, tipe in p["kolom"]]
    print(f"PRATINJAU — buat tabel '{nama_tabel}' di dokumen (docId: {doc_id}):")
    for col_id, label, tipe in p["kolom"]:
        print(f"  + kolom {col_id} [{tipe}] ({label})")
    if p["rumus"]:
        print("  Kolom rumus berikut TIDAK dibuat otomatis (isi manual di Grist setelah tabel jadi,")
        print("  tempel rumusnya dari references/rumus-umum.md - lihat SKILL.md kenapa):")
        for col_id, ket in p["rumus"].items():
            print(f"    - {col_id} -> {ket}")
    if not args.ya:
        print("\nBelum dibuat. Jalankan ulang dengan --ya setelah pengguna menjawab 'ya'.")
        return 0

    hasil = panggil_grist(base_url, kunci, f"/api/docs/{doc_id}/tables", method="POST",
                           body={"tables": [{"id": nama_tabel, "columns": kolom_req}]})
    dibuat = hasil.get("tables", [{}])[0].get("id", nama_tabel)
    print(f"BERHASIL: tabel '{dibuat}' dibuat di Grist.")
    if p["rumus"]:
        print("Langkah selanjutnya (manual, di layar Grist): tambah kolom rumus di atas lewat")
        print("'+ Add Column' > pilih 'Formula' > tempel rumus dari references/rumus-umum.md.")
    return 0


# ---------------------------------------------------------------------------
# Bersihkan & impor CSV
# ---------------------------------------------------------------------------

# --- Pembaca angka uang (v1.0.2) ---------------------------------------------------------------
# Aturan lengkap + alasan setiap keputusan ambiguitas: references/singkatan-besaran.md.
# Prinsip: nilai yang bisa dibaca DUA cara -> (None, alasan), TIDAK PERNAH ditebak.
# Semua nilai uang memakai Decimal (bukan float) supaya tidak ada galat pembulatan biner.

# Singkatan besaran (dibandingkan dalam huruf kecil). 'M' besar ditangani terpisah (case-sensitive).
_SINGKATAN = {
    "miliar": (Decimal(1_000_000_000), "miliar"),
    "milyar": (Decimal(1_000_000_000), "miliar"),
    "juta": (Decimal(1_000_000), "juta"),
    "jt": (Decimal(1_000_000), "juta"),
    "ribu": (Decimal(1_000), "ribu"),
    "rb": (Decimal(1_000), "ribu"),
    "k": (Decimal(1_000), "ribu"),
}
_POLA_SUKU = re.compile(r"(\d[\d.,]*)\s*([A-Za-z]+)")
_POLA_SUKU_PENUH = re.compile(r"(?:\s*\d[\d.,]*\s*[A-Za-z]+)+\s*")


def _pengali(satuan):
    """'jt' -> (1000000, 'juta'); 'M' -> miliar; 'm' kecil -> ('AMBIGU', ...); lainnya None."""
    if satuan == "M":
        return Decimal(1_000_000_000), "miliar"
    if satuan == "m":
        return "AMBIGU", None
    return _SINGKATAN.get(satuan.lower(), (None, None))


def _angka_sebelum_singkatan(inti, teks_asli):
    """Bagian angka di depan singkatan: '2', '1,25', '1.5'. Return (Decimal, None) / (None, alasan)."""
    if "," in inti and "." in inti:
        return None, (f"'{teks_asli}' memakai koma DAN titik sekaligus sebelum singkatan - ambigu. "
                      "Tulis satu pemisah desimal saja, mis. '1,25jt'.")
    pemisah = [c for c in inti if c in ",."]
    if len(pemisah) > 1:
        return None, (f"'{teks_asli}' punya lebih dari satu pemisah sebelum singkatan - ambigu. "
                      "Tulis angka penuh tanpa singkatan (mis. '1.250.000') atau '1,25jt'.")
    if pemisah:
        kiri, kanan = re.split(r"[.,]", inti)
        if not kiri or not kanan:
            return None, f"'{teks_asli}' tidak lengkap (ada pemisah tanpa angka di salah satu sisi)."
        if len(kanan) == 3:
            return None, (f"'{teks_asli}' ambigu: '{inti}' bisa dibaca {kiri} koma {kanan} ATAU "
                          f"{kiri}{kanan} (titik/koma ribuan). Tulis angka penuh, mis. "
                          "'1.500.000', atau pakai 1-2 angka di belakang koma, mis. '1,5jt'.")
        if len(kanan) > 3:
            return None, f"'{teks_asli}' tidak bisa dibaca: terlalu banyak angka di belakang pemisah."
        inti = f"{kiri}.{kanan}"
    return Decimal(inti), None


def _urai_singkatan(isi, teks_asli):
    """isi = teks tanpa 'Rp' & tanda minus, berisi minimal satu huruf.
    Return (Decimal, None), (None, alasan), atau (None, None) bila jelas bukan angka uang."""
    if not _POLA_SUKU_PENUH.fullmatch(isi):
        # Contoh: "Kopi Robusta", "08123 (WA)", "3jt500" (angka polos di ekor), "Gula 1kg".
        if re.fullmatch(r"(?:\s*\d[\d.,]*\s*[A-Za-z]+)+\s*\d[\d.,]*\s*", isi):
            return None, (f"'{teks_asli}' ada angka tanpa singkatan di bagian akhir - ambigu "
                          "(ribu? rupiah?). Tulis lengkap, mis. '3 jt 500 rb' atau '3.500.000'.")
        return None, None
    suku = _POLA_SUKU.findall(isi)
    total = Decimal(0)
    pengali_sebelumnya = None
    for inti, satuan in suku:
        pengali, label = _pengali(satuan)
        if pengali == "AMBIGU":
            return None, (f"'{teks_asli}' berakhiran 'm' kecil - AMBIGU (bisa meter/menit, bukan "
                          "pasti miliar). Tulis 'miliar' atau huruf BESAR 'M' (mis. '1,5M').")
        if pengali is None:
            if len(suku) == 1:
                return None, (f"'{teks_asli}': satuan '{satuan}' bukan singkatan uang yang dikenali "
                              "(yang dikenali: rb/ribu/k, jt/juta, miliar/M).")
            return None, f"'{teks_asli}': satuan '{satuan}' tidak dikenali."
        if pengali_sebelumnya is not None and pengali >= pengali_sebelumnya:
            return None, (f"'{teks_asli}' urutan singkatannya tidak turun (mis. 'rb' sebelum 'jt' "
                          "atau dobel) - ambigu. Contoh yang benar: '3 jt 500 rb'.")
        if len(suku) > 1 and not inti.isdigit():
            return None, (f"'{teks_asli}': di bentuk gabungan (mis. '3 jt 500 rb') tiap bagian harus "
                          "angka bulat tanpa koma/titik.")
        nilai, alasan = _angka_sebelum_singkatan(inti, teks_asli)
        if nilai is None:
            return None, alasan
        if pengali_sebelumnya is not None and nilai * pengali >= pengali_sebelumnya:
            return None, (f"'{teks_asli}': bagian '{inti} {satuan}' melebihi satuan di depannya - "
                          "ambigu. Tulis angka penuh, mis. '3.500.000'.")
        total += nilai * pengali
        pengali_sebelumnya = pengali
    return total, None


def _urai_angka_polos(isi, teks_asli):
    """Angka tanpa singkatan: '1.234.567,89', '1234567.89', '1.250.000', '12,5', '1,234'."""
    if not re.fullmatch(r"\d[\d.,]*", isi) or isi[-1] in ",.":
        return None, (f"'{teks_asli}' tidak bisa dibaca sebagai angka." if re.search(r"\d", isi)
                      else None)
    if "," in isi and "." in isi:
        desimal = "," if isi.rfind(",") > isi.rfind(".") else "."
        ribuan = "." if desimal == "," else ","
        if isi.count(desimal) > 1:
            return None, f"'{teks_asli}' ambigu: pemisah desimal '{desimal}' muncul lebih dari sekali."
        bulat, pecahan = isi.split(desimal)
        kelompok = bulat.split(ribuan)
    else:
        sep = "," if "," in isi else ("." if "." in isi else None)
        if sep is None:
            return Decimal(isi), None
        kelompok = isi.split(sep)
        # Satu pemisah + 1-2 angka di belakang = desimal ('12,5', '100,00', '1.5').
        if len(kelompok) == 2 and len(kelompok[1]) in (1, 2):
            return Decimal(f"{kelompok[0]}.{kelompok[1]}"), None
        # Satu pemisah + >3 angka di belakang ('1.2345') = desimal biasa (tidak mungkin ribuan).
        if len(kelompok) == 2 and len(kelompok[1]) > 3:
            return Decimal(f"{kelompok[0]}.{kelompok[1]}"), None
        pecahan = ""
    # Sisanya: pemisah ribuan -> semua kelompok setelah yang pertama WAJIB tepat 3 angka.
    if not (1 <= len(kelompok[0]) <= 3) or any(len(k) != 3 for k in kelompok[1:]):
        return None, (f"'{teks_asli}' ambigu: pengelompokan ribuan tidak konsisten "
                      "(harus per 3 angka, mis. '1.250.000').")
    return Decimal("".join(kelompok) + (f".{pecahan}" if pecahan else "")), None


def _bersihkan_angka(teks):
    """Baca teks uang/angka gaya Indonesia -> (Decimal, None), atau (None, alasan) bila teksnya
    mirip angka tapi ambigu/tidak valid, atau (None, None) bila jelas bukan angka (mis. nama barang).

    Contoh: 'Rp 1.250.000,-' -> 1250000; '1,25jt' -> 1250000; '2,5 rb' -> 2500; '10k' -> 10000;
    '3 jt 500 rb' -> 3500000; '1,5M' -> 1500000000; '1.5' dan '1,5' -> 1.5; '1.500' -> 1500
    (titik + 3 angka = ribuan, gaya Indonesia). Ditolak (ambigu): '2m' (m kecil), '1.500rb',
    '1.250,5jt', '3jt500', '1.23.456'. Rincian: references/singkatan-besaran.md.
    """
    t = teks.strip()
    if not t:
        return None, None
    isi = t
    negatif = False
    if isi.startswith("-"):
        negatif, isi = True, isi[1:].lstrip()
    isi = re.sub(r"^(?:Rp\.?|IDR)\s*", "", isi, flags=re.IGNORECASE)
    if not negatif and isi.startswith("-"):
        negatif, isi = True, isi[1:].lstrip()
    # Ekor ",-" / ".-" / ",00-" gaya kuitansi: "Rp 1.250.000,-"
    isi = re.sub(r"[.,]-$", "", isi).strip()
    if not isi or not isi[0].isdigit():
        return None, None
    if re.search(r"[A-Za-z]", isi):
        nilai, alasan = _urai_singkatan(isi, t)
    else:
        nilai, alasan = _urai_angka_polos(isi, t)
    if nilai is None:
        return None, alasan
    return (-nilai if negatif else nilai), None


def _teks_angka(nilai):
    """Decimal -> teks polos tanpa notasi ilmiah & tanpa nol berlebih: 1250000, 1234567.89."""
    teks = format(nilai, "f")
    if "." in teks:
        teks = teks.rstrip("0").rstrip(".")
    return "0" if teks in ("-0", "") else teks


def _bersihkan_header(nama):
    nama = unicodedata.normalize("NFKD", nama).encode("ascii", "ignore").decode("ascii")
    nama = re.sub(r"[^A-Za-z0-9]+", " ", nama).strip()
    kata = nama.split()
    if not kata:
        return "Kolom"
    hasil = kata[0].capitalize() + "".join(k.capitalize() for k in kata[1:])
    return hasil if re.match(r"^[A-Za-z]", hasil) else "K" + hasil


def cmd_bersihkan_csv(args):
    src = Path(args.file)
    if not src.is_file():
        raise Gagal(f"File '{src}' tidak ditemukan.", kode=2)
    with src.open(newline="", encoding="utf-8-sig") as f:
        contoh = f.read(4096)
        f.seek(0)
        try:
            dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t")
        except csv.Error:
            dialek = csv.excel
        r = csv.reader(f, dialek)
        baris = list(r)
    if not baris:
        raise Gagal("File CSV kosong.", kode=2)
    header_asli = baris[0]
    header_baru = []
    pakai = set()
    for h in header_asli:
        b = _bersihkan_header(h)
        asal, n = b, 2
        while b in pakai:
            b = f"{asal}{n}"
            n += 1
        pakai.add(b)
        header_baru.append(b)

    n_kolom = len(header_asli)
    kolom_angka = [True] * n_kolom
    kolom_ada_sukses = [False] * n_kolom  # kolom ini punya >=1 sel yang BERHASIL jadi angka
    # (nomor_baris_file, nilai_asli, alasan_atau_None) untuk tiap sel yang gagal jadi angka,
    # per kolom - dipakai buat laporan "baris mana yang menyebabkan kolom batal dikonversi"
    # (temuan SEDANG Akun B, examples/03-rekap-operasional-csv.md). Baris diberi nomor gaya file
    # CSV 1-indeks (baris 1 = header), sama seperti pesan error skill lain di repo ini.
    kolom_gagal = [[] for _ in range(n_kolom)]
    baris_bersih = []
    for no_baris, baris_asli in enumerate(baris[1:], start=2):
        baris_asli = list(baris_asli) + [""] * (n_kolom - len(baris_asli))
        baru = []
        for i, sel in enumerate(baris_asli[:n_kolom]):
            sel = sel.strip()
            if sel:
                angka, alasan = _bersihkan_angka(sel)
                if angka is None:
                    kolom_angka[i] = False
                    kolom_gagal[i].append((no_baris, sel, alasan))
                else:
                    kolom_ada_sukses[i] = True
            baru.append(sel)
        baris_bersih.append(baru)

    for baris_asli in baris_bersih:
        for i, jadi_angka in enumerate(kolom_angka):
            if jadi_angka and baris_asli[i]:
                angka, _alasan = _bersihkan_angka(baris_asli[i])
                if angka is not None:
                    baris_asli[i] = _teks_angka(angka)

    keluaran = Path(args.keluaran) if args.keluaran else src.with_name(src.stem + "-bersih.csv")
    with keluaran.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header_baru)
        w.writerows(baris_bersih)

    # Kolom yang batal jadi Numeric PADAHAL sebagian selnya berhasil dibaca sebagai angka -> ini
    # yang perlu disebut baris penyebabnya (bukan kolom teks murni seperti "Nama Barang", yang
    # memang tidak ada sel angkanya sama sekali - itu bukan "kegagalan", cuma memang kolom teks).
    peringatan_kolom_gagal = []
    for i, h_asli in enumerate(header_asli):
        if kolom_angka[i] or not kolom_ada_sukses[i] or not kolom_gagal[i]:
            continue
        contoh = kolom_gagal[i][:5]
        rincian = "; ".join(
            f"baris {n}: {v!r}" + (f" ({a})" if a else "") for n, v, a in contoh)
        lebih = "" if len(kolom_gagal[i]) <= 5 else f"; +{len(kolom_gagal[i]) - 5} baris lain"
        peringatan_kolom_gagal.append(
            f"Kolom {h_asli!r} SEBAGIAN selnya angka tapi TETAP jadi Text karena {rincian}{lebih}. "
            "Kolom ini TIDAK dirapikan sama sekali (semua baris, termasuk yang tadinya berhasil, "
            "dibiarkan apa adanya) - benarkan dulu sel di atas lalu jalankan ulang, atau abaikan "
            "kalau memang mau kolom ini tetap Text.")

    print(f"SELESAI membersihkan '{src.name}' -> '{keluaran}'")
    print(f"Baris data: {len(baris_bersih)}")
    print("Kolom (nama asli -> nama Grist, jenis):")
    for h_asli, h_baru, angka in zip(header_asli, header_baru, kolom_angka):
        print(f"  - {h_asli!r} -> {h_baru}  ({'Numeric' if angka else 'Text'})")
    print("Angka Rupiah/desimal dirapikan jadi angka polos (mis. 'Rp 1.234.567,89' -> 1234567.89;")
    print("singkatan 'ribu'/'rb'/'k', 'juta'/'jt', 'miliar'/'M' & gabungan '3 jt 500 rb' juga didukung;")
    print("nilai ambigu seperti '1.500rb' atau '2m' TIDAK ditebak - disebut baris & alasannya di bawah).")
    if peringatan_kolom_gagal:
        print("\nPERINGATAN - kolom sebagian angka tapi dibiarkan Text (perbaiki sel di bawah lalu ulangi):")
        for p in peringatan_kolom_gagal:
            print(f"  - {p}")
    print("\nPeriksa dulu file hasil sebelum diimpor. Lanjut: 'impor-csv' (perlu REST API) atau")
    print("seret file ini ke Grist lewat menu Import (selalu tersedia, tanpa API).")
    if args.json:
        print(json.dumps({
            "keluaran": str(keluaran), "baris": len(baris_bersih), "kolom": header_baru,
            "kolom_gagal_sebagian": [
                {"kolom": header_asli[i], "gagal": [
                    {"baris": n, "nilai": v, "alasan": a} for n, v, a in kolom_gagal[i]]}
                for i in range(n_kolom) if not kolom_angka[i] and kolom_ada_sukses[i] and kolom_gagal[i]
            ],
        }, ensure_ascii=False))
    return 0


def cmd_impor_csv(args):
    src = Path(args.file)
    if not src.is_file():
        raise Gagal(f"File '{src}' tidak ditemukan.", kode=2)
    with src.open(newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        baris = list(r)
        header = r.fieldnames or []
    if not baris:
        raise Gagal("File CSV tidak berisi baris data (hanya header, atau kosong).", kode=2)
    for h in header:
        if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", h):
            raise Gagal(f"Nama kolom '{h}' tidak sesuai aturan Grist (harus diawali huruf, hanya "
                        "huruf/angka/garis bawah). Jalankan 'bersihkan-csv' dulu.", kode=2)

    base_url = ambil_base_url(args.url)
    kunci = ambil_kunci(args.kunci_file)
    doc_id = cari_dokumen(base_url, kunci, args.dokumen)

    print(f"PRATINJAU — impor {len(baris)} baris dari '{src.name}' ke tabel '{args.tabel}' "
          f"(docId: {doc_id}):")
    print(f"Kolom: {', '.join(header)}")
    for contoh in baris[:3]:
        print(f"  contoh: {dict(contoh)}")
    if len(baris) > 3:
        print(f"  ... dan {len(baris) - 3} baris lagi")
    print("\nCatatan: tabel & kolom di atas HARUS SUDAH ADA di Grist (buat dulu dengan 'buat-tabel'")
    print("atau manual di Grist). Perintah ini hanya MENAMBAH baris baru, tidak membuat kolom.")
    if not args.ya:
        print("\nBelum diimpor. Jalankan ulang dengan --ya setelah pengguna menjawab 'ya'.")
        return 0

    records = [{"fields": dict(b)} for b in baris]
    hasil = panggil_grist(base_url, kunci, f"/api/docs/{doc_id}/tables/{args.tabel}/records",
                           method="POST", body={"records": records})
    n = len(hasil.get("records", []))
    print(f"BERHASIL: {n} baris ditambahkan ke tabel '{args.tabel}'.")
    return 0


# ---------------------------------------------------------------------------
# Baca file .grist (SQLite) — SELALU read-only
# ---------------------------------------------------------------------------

def _buka_ro(path):
    p = Path(path)
    if not p.is_file():
        raise Gagal(f"File '{p}' tidak ditemukan.", kode=2)
    uri = "file:" + urllib.parse.quote(str(p.resolve())) + "?mode=ro"
    try:
        con = sqlite3.connect(uri, uri=True)
        con.execute("PRAGMA query_only = 1")
        con.execute("SELECT 1 FROM sqlite_master LIMIT 1")
    except sqlite3.Error as e:
        raise Gagal(f"'{p}' tidak bisa dibuka sebagai file Grist (rusak, bukan file .grist, atau "
                    f"sedang dipakai program lain): {e}", kode=3) from None
    return con


def _daftar_tabel_pengguna(con):
    """Kembalikan list (tableId, jumlah_kolom) dari metadata resmi Grist (_grist_Tables /
    _grist_Tables_column), BUKAN tabel _grist*/_gristsys* internal."""
    ada_meta = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='_grist_Tables'"
    ).fetchone()
    if not ada_meta:
        raise Gagal("File ini tidak punya tabel metadata '_grist_Tables' - kemungkinan bukan file "
                    ".grist asli, atau rusak.", kode=3)
    tabel = con.execute("SELECT id, tableId FROM _grist_Tables ORDER BY id").fetchall()
    hasil = []
    for tid, table_id in tabel:
        n_kolom = con.execute(
            "SELECT COUNT(*) FROM _grist_Tables_column WHERE parentId = ?", (tid,)
        ).fetchone()[0]
        hasil.append((table_id, n_kolom))
    return hasil


def cmd_daftar_tabel(args):
    con = _buka_ro(args.file)
    try:
        tabel = _daftar_tabel_pengguna(con)
    finally:
        con.close()
    print(f"TABEL DI '{Path(args.file).name}' ({len(tabel)}):")
    for table_id, n_kolom in tabel:
        print(f"  - {table_id}  ({n_kolom} kolom)")
    if not tabel:
        print("  (belum ada tabel pengguna - dokumen masih kosong)")
    if args.json:
        print(json.dumps([{"tabel": t, "kolom": n} for t, n in tabel], ensure_ascii=False))
    return 0


def _kolom_tabel(con, table_id):
    baris = con.execute(
        "SELECT c.colId, c.type, c.isFormula, c.label FROM _grist_Tables_column c "
        "JOIN _grist_Tables t ON t.id = c.parentId WHERE t.tableId = ? ORDER BY c.parentPos",
        (table_id,),
    ).fetchall()
    if baris is None:
        return []
    return baris


def _pastikan_tabel_ada(con, table_id):
    ok = con.execute("SELECT 1 FROM _grist_Tables WHERE tableId = ?", (table_id,)).fetchone()
    if not ok:
        nama = [t for t, _ in _daftar_tabel_pengguna(con)]
        raise Gagal(f"Tabel '{table_id}' tidak ada. Tabel yang ada: {', '.join(nama) or '(tidak ada)'}", kode=2)


def cmd_ringkasan(args):
    con = _buka_ro(args.file)
    try:
        _pastikan_tabel_ada(con, args.tabel)
        kolom = _kolom_tabel(con, args.tabel)
        try:
            jumlah = con.execute(f'SELECT COUNT(*) FROM "{args.tabel}"').fetchone()[0]
        except sqlite3.Error as e:
            raise Gagal(f"Tabel '{args.tabel}' terdaftar di metadata tapi datanya tidak terbaca "
                        f"(file kemungkinan rusak/setengah tersalin): {e}", kode=3) from None
        nama_kolom = [c for c, *_ in kolom]
        contoh = []
        if nama_kolom:
            kolom_sql = ", ".join(f'"{c}"' for c in nama_kolom)
            contoh = con.execute(f'SELECT {kolom_sql} FROM "{args.tabel}" LIMIT ?', (args.n,)).fetchall()
    finally:
        con.close()

    print(f"RINGKASAN TABEL '{args.tabel}'")
    print(f"Jumlah baris: {jumlah}")
    print(f"Kolom ({len(kolom)}):")
    for col_id, tipe, is_formula, label in kolom:
        print(f"  - {col_id:20s} [{tipe or '?':10s}] {'(rumus)' if is_formula else '':8s} label: {label}")
    if contoh:
        print(f"\nContoh {len(contoh)} baris pertama:")
        for baris in contoh:
            print(f"  {dict(zip(nama_kolom, baris))}")
    if args.json:
        print(json.dumps({
            "tabel": args.tabel, "jumlah_baris": jumlah,
            "kolom": [{"id": c, "tipe": t, "rumus": bool(f), "label": l} for c, t, f, l in kolom],
            "contoh": [dict(zip(nama_kolom, b)) for b in contoh],
        }, ensure_ascii=False, default=str))
    return 0


def cmd_ekspor_csv(args):
    con = _buka_ro(args.file)
    try:
        _pastikan_tabel_ada(con, args.tabel)
        kolom = [c for c, *_ in _kolom_tabel(con, args.tabel)]
        if not kolom:
            raise Gagal(f"Tabel '{args.tabel}' tidak punya kolom pengguna (kosong).", kode=2)
        kolom_sql = ", ".join(f'"{c}"' for c in kolom)
        try:
            baris = con.execute(f'SELECT {kolom_sql} FROM "{args.tabel}" ORDER BY id').fetchall()
        except sqlite3.Error as e:
            raise Gagal(f"Tidak bisa membaca isi tabel '{args.tabel}' (file kemungkinan rusak): {e}", kode=3) from None
    finally:
        con.close()

    keluaran = Path(args.keluaran) if args.keluaran else Path(f"{args.tabel}.csv")
    with keluaran.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(kolom)
        w.writerows(baris)
    print(f"SELESAI: {len(baris)} baris dari tabel '{args.tabel}' ditulis ke '{keluaran}'.")
    if args.json:
        print(json.dumps({"keluaran": str(keluaran), "baris": len(baris)}, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------

def _opsi_umum(p):
    p.add_argument("--url", help="Alamat Grist (default: http://localhost:8484 atau ENV GRIST_URL)")
    p.add_argument("--kunci-file", help="Path file kunci API (default: ~/.komunitech/grist-kunci.txt)")
    p.add_argument("--json", action="store_true", help="Cetak juga hasil sebagai JSON")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="grist.py", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="perintah", required=True)

    p = sub.add_parser("cek", help="Cek koneksi REST API & daftar dokumen yang bisa diakses")
    _opsi_umum(p)
    p.set_defaults(fungsi=cmd_cek)

    p = sub.add_parser("simpan-kunci", help="Simpan kunci API Grist (ditanya lewat prompt, tidak terlihat)")
    p.add_argument("--kunci-file", help="Simpan ke path lain (default: ~/.komunitech/grist-kunci.txt)")
    p.add_argument("--ya", action="store_true", help="Timpa file kunci yang sudah ada")
    p.set_defaults(fungsi=cmd_simpan_kunci)

    p_pola = sub.add_parser("pola", help="Pola tabel siap pakai untuk UMKM")
    sub_pola = p_pola.add_subparsers(dest="aksi_pola", required=True)
    p2 = sub_pola.add_parser("daftar", help="Daftar semua pola")
    p2.set_defaults(fungsi=cmd_pola_daftar)
    p2 = sub_pola.add_parser("tampilkan", help="Detail satu pola")
    p2.add_argument("nama", choices=list(POLA_TABEL))
    p2.set_defaults(fungsi=cmd_pola_tampilkan)

    p = sub.add_parser("buat-tabel", help="Buat tabel dari pola siap pakai lewat REST API (perlu kunci)")
    p.add_argument("pola", choices=list(POLA_TABEL))
    p.add_argument("--dokumen", required=True, help="Nama dokumen Grist, atau docId")
    p.add_argument("--tabel", help="Nama tabel (default: nama bawaan pola)")
    p.add_argument("--ya", action="store_true", help="Benar-benar buat (tanpa ini hanya pratinjau)")
    _opsi_umum(p)
    p.set_defaults(fungsi=cmd_buat_tabel)

    p = sub.add_parser("bersihkan-csv", help="Rapikan angka Rupiah/nama kolom CSV sebelum diimpor ke Grist")
    p.add_argument("file")
    p.add_argument("--keluaran", help="Nama file CSV hasil (default: <nama>-bersih.csv)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fungsi=cmd_bersihkan_csv)

    p = sub.add_parser("impor-csv", help="Impor baris CSV ke tabel Grist yang SUDAH ADA lewat REST API")
    p.add_argument("file")
    p.add_argument("--dokumen", required=True, help="Nama dokumen Grist, atau docId")
    p.add_argument("--tabel", required=True, help="Nama tabel tujuan (harus sudah ada)")
    p.add_argument("--ya", action="store_true", help="Benar-benar impor (tanpa ini hanya pratinjau)")
    _opsi_umum(p)
    p.set_defaults(fungsi=cmd_impor_csv)

    p = sub.add_parser("daftar-tabel", help="Baca file .grist (read-only): daftar tabel")
    p.add_argument("file", help="Path file .grist")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fungsi=cmd_daftar_tabel)

    p = sub.add_parser("ringkasan", help="Baca file .grist (read-only): ringkasan satu tabel")
    p.add_argument("file", help="Path file .grist")
    p.add_argument("tabel", help="Nama tabel (tableId, sesuai di Grist)")
    p.add_argument("--n", type=int, default=5, help="Jumlah baris contoh (default 5)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fungsi=cmd_ringkasan)

    p = sub.add_parser("ekspor-csv", help="Baca file .grist (read-only): ekspor satu tabel ke CSV")
    p.add_argument("file", help="Path file .grist")
    p.add_argument("tabel", help="Nama tabel (tableId, sesuai di Grist)")
    p.add_argument("--keluaran", help="Nama file CSV hasil (default: <tabel>.csv)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fungsi=cmd_ekspor_csv)

    args = ap.parse_args(argv)
    try:
        return args.fungsi(args)
    except Gagal as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return e.kode
    except KeyboardInterrupt:
        print("\nDibatalkan.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
