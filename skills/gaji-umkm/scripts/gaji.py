#!/usr/bin/env python3
"""gaji-umkm (Komunitech) - aplikasi penggajian bulanan lokal untuk UMKM (5-50 karyawan).

Satu file database SQLite di komputer pemilik. Hanya library standar Python 3.8+, lintas OS
(Windows: `python`/`py`), TANPA akses jaringan dan TANPA koneksi ke bank.

Semua angka gaji, BPJS, PPh 21, dan THR dihitung oleh salinan PERSIS script skill Komunitech lain
di folder mesin/ (lihat mesin/SUMBER.json):
  - mesin/payroll.py  = slip-gaji-bpjs (BPJS, lembur PP 35/2021, PPh 21 TER, take home pay)
  - mesin/pph21.py    = pph21-ter      (cek ulang PPh 21 setahun)
  - mesin/thr.py      = hitung-thr     (THR Keagamaan)
gaji.py hanya menyimpan data (karyawan, periode, riwayat), menyusun masukan, menjalankan mesin lewat
subprocess (--format json), lalu menyimpan & menampilkan hasilnya. gaji.py tidak punya tarif sendiri.

Lokasi database (urutan prioritas):
  1. --db PATH (ditulis setelah nama perintah)
  2. ENV KOMUNITECH_GAJI_DB  (path file lengkap)
  3. ENV KOMUNITECH_DATA     (folder) + /gaji/gaji.db
  4. ~/KomunitechData/gaji/gaji.db
Cadangan: folder backup-gaji/ di sebelah database.

Perubahan besar (init, karyawan tambah/ubah/keluar/impor, impor-absensi, isi --file, thr, final, revisi,
restore) hanya PRATINJAU sampai diberi --ya. Perubahan kecil (isi satu karyawan, saldo-awal, atur, hitung)
langsung tersimpan (hanya berlaku untuk periode yang belum final).

Kode keluar: 0 = berhasil; 1 = gagal (pesan jelas di "error"/stderr); 2 = perintah salah tulis.
"""
import argparse
import calendar
import csv
import hashlib
import io
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

VERSI = "1.0.13"
APLIKASI = "gaji-umkm"
SKEMA = 1
FOLDER = Path(__file__).resolve().parent
MESIN = FOLDER / "mesin"
sys.path.insert(0, str(MESIN))
sys.dont_write_bytecode = True          # jangan menulis __pycache__ ke folder mesin/
import ter_core as tc  # noqa: E402  (salinan persis; hanya dipakai untuk baca angka & format rupiah)

SIMPAN_BACKUP_HARIAN = 30
NOL = Decimal(0)
DISCLAIMER = ("Alat bantu hitung, bukan nasihat hukum/pajak. Angka dari mesin hitung gaji, PPh 21 dan THR Komunitech. "
              "Dasar: Perpres 64/2020; PP 44, 45, 46/2015 & PP 6/2025 (BPJS); PP 35/2021 "
              "(lembur); PP 58/2023 & PMK 168/2023 (PPh 21); PMK 105/2025 (DTP); Permenaker 6/2016 (THR); berlaku per "
              "23 September 2026. Pembulatan: iuran BPJS & lembur ke "
              "rupiah terdekat, PPh 21 ke bawah; belum dicocokkan dengan Coretax/aplikasi BPJS - bila berbeda, ikuti "
              "sistem resmi. Kasus khusus: konsultan pajak, Kring Pajak 1500200, BPJS, atau Disnaker.")
PESAN_TERKUNCI = ("Database sedang dipakai program lain (mis. jadwal OpenClaw). Data aman; tunggu sebentar lalu "
                  "ulangi perintahnya.")
SARAN_PULIH = ("Pulihkan: gaji.py backup --daftar (lihat cadangan), lalu gaji.py restore --dari <file cadangan> "
               "(pratinjau, lalu --ya). Jangan hapus file database.")

# kolom isian per periode (komponen tidak tetap & penyesuaian bulan itu)
ISIAN = {
    "tunjangan_tidak_tetap": ("uang", "Tunjangan tidak tetap (uang makan/transport bulan ini)"),
    "lembur_hari_kerja": ("jam", "Jam lembur hari kerja (per hari, dipisah +)"),
    "lembur_hari_libur": ("jam", "Jam lembur hari libur/istirahat (per hari, dipisah +; akhiran p = hari kerja terpendek)"),
    "lembur_rp": ("uang", "Nominal lembur jadi (bila tidak memakai jam)"),
    "bonus": ("uang", "Bonus/insentif"),
    "thr": ("uang", "THR"),
    "potongan_lain": ("uang", "Potongan lain (kasbon, cicilan, dll.)"),
    "potongan_tidak_masuk": ("uang", "Potongan tidak masuk (hanya bila diatur di PK/PP/PKB)"),
    "zakat": ("uang", "Zakat lewat perusahaan (ganti nilai tetap bulanan)"),
    "gaji_pokok": ("uang", "Gaji pokok yang dibayar bulan ini (mis. prorata masuk/keluar tengah bulan)"),
    "tunjangan_tetap": ("uang", "Tunjangan tetap yang dibayar bulan ini (mis. prorata)"),
    "hari_hadir": ("info", "Hari hadir (dari absensi)"),
    "hari_alpa": ("info", "Hari alpa/tanpa keterangan (dari absensi)"),
    "terlambat_menit": ("info", "Total menit terlambat (dari absensi)"),
    "catatan": ("teks", "Catatan"),
}
OPSI_ISIAN = {k.replace("_", "-"): k for k in ISIAN}
OPSI_ISIAN.update({"kasbon": "potongan_lain", "gaji-pokok-dibayar": "gaji_pokok",
                   "tunjangan-tetap-dibayar": "tunjangan_tetap"})

SKEMA_SQL = """
CREATE TABLE meta(kunci TEXT PRIMARY KEY, nilai TEXT NOT NULL DEFAULT '');
CREATE TABLE karyawan(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kode TEXT NOT NULL UNIQUE,
  nama TEXT NOT NULL,
  jabatan TEXT NOT NULL DEFAULT '',
  jenis TEXT NOT NULL DEFAULT 'tetap',
  ptkp TEXT NOT NULL,
  gaji_pokok TEXT NOT NULL,
  tunjangan_tetap TEXT NOT NULL DEFAULT '0',
  tunjangan_tidak_tetap TEXT NOT NULL DEFAULT '0',
  zakat TEXT NOT NULL DEFAULT '0',
  ikut_kes INTEGER NOT NULL DEFAULT 1,
  ikut_tk INTEGER NOT NULL DEFAULT 1,
  ikut_jp INTEGER NOT NULL DEFAULT 1,
  jkk_persen TEXT NOT NULL DEFAULT '',
  hari_kerja INTEGER NOT NULL DEFAULT 5,
  dasar_bpjs_kesehatan TEXT NOT NULL DEFAULT '',
  dtp INTEGER NOT NULL DEFAULT 0,
  bruto_tetap_januari TEXT NOT NULL DEFAULT '',
  nik TEXT NOT NULL DEFAULT '',
  bank TEXT NOT NULL DEFAULT '',
  rekening TEXT NOT NULL DEFAULT '',
  atas_nama TEXT NOT NULL DEFAULT '',
  kode_absensi TEXT NOT NULL DEFAULT '',
  tanggal_masuk TEXT NOT NULL,
  tanggal_keluar TEXT NOT NULL DEFAULT '',
  dibuat TEXT NOT NULL,
  diubah TEXT NOT NULL
);
CREATE TABLE saldo_awal(
  karyawan_id INTEGER NOT NULL, tahun INTEGER NOT NULL, sampai_bulan INTEGER NOT NULL,
  bruto TEXT NOT NULL, pph21 TEXT NOT NULL, iuran TEXT NOT NULL, zakat TEXT NOT NULL DEFAULT '0',
  PRIMARY KEY(karyawan_id, tahun)
);
CREATE TABLE periode(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kode TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'draf',
  revisi INTEGER NOT NULL DEFAULT 0,
  dibuat TEXT NOT NULL,
  difinalkan TEXT NOT NULL DEFAULT ''
);
CREATE TABLE isian(
  periode_id INTEGER NOT NULL, karyawan_id INTEGER NOT NULL, kolom TEXT NOT NULL, nilai TEXT NOT NULL,
  keterangan TEXT NOT NULL DEFAULT '',
  PRIMARY KEY(periode_id, karyawan_id, kolom)
);
CREATE TABLE hasil(
  periode_id INTEGER NOT NULL, revisi INTEGER NOT NULL, karyawan_id INTEGER NOT NULL, data TEXT NOT NULL,
  PRIMARY KEY(periode_id, revisi, karyawan_id)
);
CREATE TABLE hasil_periode(
  periode_id INTEGER NOT NULL, revisi INTEGER NOT NULL, dihitung TEXT NOT NULL, sidik TEXT NOT NULL,
  total TEXT NOT NULL, peringatan TEXT NOT NULL,
  PRIMARY KEY(periode_id, revisi)
);
CREATE TABLE revisi(
  id INTEGER PRIMARY KEY AUTOINCREMENT, periode_id INTEGER NOT NULL, nomor INTEGER NOT NULL, dibuka TEXT NOT NULL,
  alasan TEXT NOT NULL, difinalkan TEXT NOT NULL DEFAULT '', selisih TEXT NOT NULL DEFAULT ''
);
CREATE TABLE log(id INTEGER PRIMARY KEY AUTOINCREMENT, waktu TEXT, perintah TEXT, ringkasan TEXT);
"""
PENGATURAN_DEFAULT = {"nama_usaha": "", "umk": "", "jkk": "", "batas_jp": "", "tanggal_gajian": "25",
                      "potongan_per_hari_alpa": "", "dasar_potongan": ""}


class Gagal(Exception):
    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


# --------------------------------------------------------------------------- waktu & angka
_JAM = {"hari_ini": None}


def hari_ini():
    return _JAM["hari_ini"] or date.today()


def stempel():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def D(x):
    if x is None or x == "":
        return NOL
    return Decimal(str(x))


def rp(x):
    return tc.format_rp(D(x))


def uang(nilai, nama):
    """Nominal rupiah format Indonesia -> Decimal bulat (rupiah terdekat), tidak negatif."""
    try:
        d = tc.parse_angka(nilai, nama)
    except ValueError as e:
        raise Gagal(str(e))
    return tc.bulat_terdekat(d)


def teks_angka(d):
    """Decimal -> teks tanpa pemisah ribuan & dengan titik desimal (aman untuk CSV mesin)."""
    d = D(d)
    if d == d.to_integral_value():
        return str(int(d))
    return "{:f}".format(d.normalize())


def persen(nilai, nama):
    try:
        d = tc.parse_angka(nilai, nama)
    except ValueError as e:
        raise Gagal(str(e))
    if not NOL < d <= 10:
        raise Gagal("%s harus lebih dari 0 dan paling besar 10 (persen), mis. 0,54" % nama)
    return d


def tanggal(teks, nama="tanggal"):
    s = str(teks or "").strip().lower()
    if not s:
        raise Gagal("%s kosong" % nama)
    if s in ("hari-ini", "hari ini", "sekarang"):
        return hari_ini()
    for pola in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, pola).date()
        except ValueError:
            continue
    raise Gagal("%s '%s' tidak dikenali. Tulis 2026-09-14 atau 14/09/2026." % (nama, teks))


def parse_periode(teks):
    s = str(teks or "").strip().lower()
    if s in ("ini", "bulan-ini", "bulan ini"):
        h = hari_ini()
        return "%04d-%02d" % (h.year, h.month)
    if s in ("lalu", "bulan-lalu", "bulan lalu"):
        h = hari_ini().replace(day=1) - timedelta(days=1)
        return "%04d-%02d" % (h.year, h.month)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", s) or None
    if m:
        th, bl = int(m.group(1)), int(m.group(2))
    else:
        m = re.fullmatch(r"(\d{1,2})[/-](\d{4})", s)
        if not m:
            raise Gagal("Periode '%s' tidak dikenali. Tulis YYYY-MM, mis. 2026-09." % teks)
        th, bl = int(m.group(2)), int(m.group(1))
    if not (1 <= bl <= 12 and 2000 <= th <= 2100):
        raise Gagal("Periode '%s' tidak valid." % teks)
    return "%04d-%02d" % (th, bl)


def rentang_periode(kode):
    th, bl = int(kode[:4]), int(kode[5:7])
    return date(th, bl, 1), date(th, bl, calendar.monthrange(th, bl)[1])


def nama_periode(kode):
    return "%s %s" % (tc.NAMA_BULAN[int(kode[5:7]) - 1], kode[:4])


def ftgl(d):
    return d.strftime("%d/%m/%Y") if isinstance(d, date) else str(d)


def ya_tidak(nilai, nama):
    s = str(nilai or "").strip().lower()
    if s in ("ya", "y", "yes", "true", "1", "iya"):
        return True
    if s in ("tidak", "t", "no", "n", "false", "0", "tdk", "gak", "nggak"):
        return False
    raise Gagal("%s: isi 'ya' atau 'tidak' (bukan '%s')" % (nama, nilai))


def bersih(teks, maks=120):
    s = re.sub(r"[\x00-\x1f\x7f]", " ", str(teks or "")).strip()
    return re.sub(r"\s+", " ", s)[:maks]


# --------------------------------------------------------------------------- data pribadi
def samarkan(nomor):
    s = re.sub(r"\D", "", str(nomor or ""))
    if not s:
        return ""
    if len(s) <= 4:
        return "*" * len(s)
    return "*" * (len(s) - 4) + s[-4:]


def cek_nik(teks):
    s = re.sub(r"[\s.\-]", "", str(teks or ""))
    if not s:
        return ""
    if not re.fullmatch(r"\d{16}", s):
        raise Gagal("NIK harus 16 angka (boleh dikosongkan; NIK tidak wajib).")
    return s


def cek_rekening(teks):
    s = re.sub(r"[\s.\-]", "", str(teks or ""))
    if not s:
        return ""
    if re.search(r"[eE]\+?\d", s):
        raise Gagal("Nomor rekening '%s' rusak karena Excel (format ilmiah). Ketik ulang sebagai teks." % teks)
    if not re.fullmatch(r"\d{5,20}", s):
        raise Gagal("Nomor rekening harus 5-20 angka (boleh dikosongkan).")
    return s


# --------------------------------------------------------------------------- database
def path_db(args):
    if getattr(args, "db", None):
        p = Path(args.db).expanduser()
    elif os.environ.get("KOMUNITECH_GAJI_DB"):
        p = Path(os.environ["KOMUNITECH_GAJI_DB"]).expanduser()
    elif os.environ.get("KOMUNITECH_DATA"):
        p = Path(os.environ["KOMUNITECH_DATA"]).expanduser() / "gaji" / "gaji.db"
    else:
        p = Path.home() / "KomunitechData" / "gaji" / "gaji.db"
    return p.resolve()


def folder_backup(db):
    return db.parent / "backup-gaji"


def _terkunci(e):
    return "locked" in str(e).lower() or "busy" in str(e).lower()


def sambung(db, ro=False):
    try:
        if ro:
            c = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True, timeout=10, isolation_level=None)
        else:
            c = sqlite3.connect(str(db), timeout=10, isolation_level=None)
    except sqlite3.OperationalError as e:
        raise Gagal("Database %s tidak bisa dibuka (%s). Periksa folder dan izin aksesnya." % (db, e))
    c.row_factory = sqlite3.Row
    return c


def buka(db, baca_saja=False):
    if not db.is_file():
        raise Gagal("Database gaji belum ada di %s. Jalankan dulu: gaji.py init (lalu --ya setelah pengguna setuju)."
                    % db, belum_ada=True)
    if db.stat().st_size == 0:
        raise Gagal("File %s kosong (0 byte). %s" % (db, SARAN_PULIH), rusak=True)
    ro = baca_saja
    while True:
        conn = sambung(db, ro)
        try:
            r = conn.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
            sk = conn.execute("SELECT nilai FROM meta WHERE kunci='skema'").fetchone()
            break
        except sqlite3.OperationalError as e:
            conn.close()
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI)
            if ro and "readonly" in str(e).lower():
                ro = False
                continue
            if "no such table" in str(e).lower():
                raise Gagal("File %s bukan database gaji-umkm. File itu tidak diubah; periksa --db." % db)
            raise Gagal("Database %s tidak bisa dibaca (%s). %s" % (db, e, SARAN_PULIH), rusak=True)
        except sqlite3.DatabaseError:
            conn.close()
            raise Gagal("File %s rusak atau bukan database gaji-umkm. %s" % (db, SARAN_PULIH), rusak=True)
    if not r or r[0] != APLIKASI:
        conn.close()
        raise Gagal("File %s bukan database gaji-umkm. File itu tidak diubah; periksa --db." % db)
    if sk and str(sk[0]).isdigit() and int(sk[0]) > SKEMA:
        conn.close()
        raise Gagal("Database dibuat oleh gaji-umkm versi lebih baru (skema %s). Perbarui skill dulu." % sk[0])
    return conn


def pengaturan(conn):
    cfg = dict(PENGATURAN_DEFAULT)
    for r in conn.execute("SELECT kunci, nilai FROM meta"):
        cfg[r[0]] = r[1]
    return cfg


def nama_unik(folder, dasar, akhiran=".db"):
    tujuan = folder / (dasar + akhiran)
    n = 2
    while tujuan.exists():
        tujuan = folder / ("%s-%d%s" % (dasar, n, akhiran))
        n += 1
    return tujuan


def buat_backup(db, label):
    if not db.is_file():
        return None
    fol = folder_backup(db)
    fol.mkdir(parents=True, exist_ok=True)
    tujuan = nama_unik(fol, "gaji-%s-%s" % (datetime.now().strftime("%Y%m%d-%H%M%S"), label))
    src = sqlite3.connect(str(db), timeout=10)
    dst = sqlite3.connect(str(tujuan))
    try:
        src.backup(dst)
    except sqlite3.OperationalError as e:
        dst.close()
        try:
            tujuan.unlink()
        except OSError:
            pass
        if _terkunci(e):
            raise Gagal(PESAN_TERKUNCI)
        raise
    finally:
        dst.close()
        src.close()
    return str(tujuan)


def backup_harian(db):
    fol = folder_backup(db)
    awalan = "gaji-%s-" % datetime.now().strftime("%Y%m%d")
    if fol.is_dir() and any(p.name.startswith(awalan) for p in fol.glob("gaji-*.db")):
        return None
    b = buat_backup(db, "harian")
    harian = sorted(fol.glob("gaji-*-harian*.db"))
    for lama in harian[:-SIMPAN_BACKUP_HARIAN]:
        try:
            lama.unlink()
        except OSError:
            pass
    return b


def jalankan_tulis(args, perintah, kerja, besar=False, label_backup=None):
    """kerja(conn, cfg) -> (data, teks). besar=True: tanpa --ya hanya pratinjau (ROLLBACK)."""
    db = path_db(args)
    conn = buka(db)
    simpan = bool(getattr(args, "ya", False)) or not besar
    backup = None
    try:
        if simpan:
            backup = buat_backup(db, label_backup) if (besar and label_backup) else backup_harian(db)
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as e:
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI)
            raise
        try:
            data, teks = kerja(conn, pengaturan(conn))
            if simpan:
                conn.execute("INSERT INTO log(waktu, perintah, ringkasan) VALUES (?,?,?)",
                             (stempel(), perintah, json.dumps(data.get("ringkasan", {}), ensure_ascii=False,
                                                              default=str)[:2000]))
                conn.execute("COMMIT")
            else:
                conn.execute("ROLLBACK")
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
    finally:
        conn.close()
    data.setdefault("ok", True)
    data.setdefault("peringatan", [])
    data["mode"] = "tersimpan" if simpan else "pratinjau"
    data["perlu_konfirmasi"] = not simpan
    data["db"] = str(db)
    if backup:
        data["backup"] = backup
    if data["peringatan"]:
        teks += "\n\n" + "\n".join("Catatan: " + p for p in data["peringatan"])
    langkah = data.setdefault("langkah_berikut", [])
    if simpan and besar:
        teks = "TERSIMPAN.\n" + teks + ("\n(Cadangan otomatis dibuat sebelum perubahan.)" if backup else "")
    elif not simpan and data.get("perlu_persetujuan_khusus"):
        # teks untuk pemilik tanpa nama perintah/opsi; instruksi menyimpan hanya untuk agent (langkah_berikut)
        teks = ("PRATINJAU (belum disimpan):\n" + teks + "\n\n" + PENUTUP_PERSETUJUAN)
        langkah.insert(0, LANGKAH_PERSETUJUAN)
    elif not simpan:
        teks = "PRATINJAU (belum disimpan):\n" + teks + "\n\n" + penutup_pratinjau(perintah)
        langkah.insert(0, LANGKAH_SIMPAN)
    data["teks"] = teks
    return data, teks


LANGKAH_SIMPAN = "Simpan hanya setelah pemilik setuju: jalankan perintah yang sama + --ya."
LANGKAH_PERSETUJUAN = (
    "BELUM BISA DISIMPAN DENGAN --ya SAJA: data ini butuh persetujuan khusus pemilik (masalah_kepatuhan). Sarankan "
    "memperbaiki datanya. Hanya bila pemilik sendiri sudah membaca peringatan dan menyetujuinya dengan alasan sah: "
    "jalankan perintah yang sama + --ya --ya-saya-paham --alasan-khusus \"...\" (dicatat di log). Jangan menambahkan "
    "--ya-saya-paham atas inisiatif sendiri.")
PENUTUP_PERSETUJUAN = ("Belum bisa disimpan begitu saja: data ini perlu persetujuan khusus pemilik (lihat PERLU "
                       "PERSETUJUAN KHUSUS di atas). Sebaiknya datanya diperbaiki; bila ada alasan sah, sebutkan "
                       "alasannya dan nyatakan setuju.")


def penutup_pratinjau(perintah):
    """Kalimat penutup pratinjau untuk pemilik (tanpa nama perintah/opsi)."""
    if perintah == "final":
        return "Sudah benar? Balas \"kunci\" - setelah dikunci, angka bulan ini hanya bisa diubah lewat revisi tercatat."
    if perintah == "restore":
        return "Lanjut memulihkan? Balas \"pulihkan\"."
    if perintah == "revisi":
        return "Buka revisi? Balas \"ya\"."
    return "Sudah benar? Balas \"simpan\" untuk menyimpan."


def baca(args, kerja):
    conn = buka(path_db(args), baca_saja=True)
    try:
        data, teks = kerja(conn, pengaturan(conn))
    finally:
        conn.close()
    data.setdefault("ok", True)
    data.setdefault("mode", "baca")
    data["teks"] = teks
    return data, teks


# --------------------------------------------------------------------------- mesin (script skill sumber)
def cek_mesin():
    try:
        manifest = json.loads((MESIN / "SUMBER.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise Gagal("File mesin/SUMBER.json hilang/rusak. Pasang ulang skill gaji-umkm dari paket aslinya.")
    for nama, info in manifest["file"].items():
        p = MESIN / nama
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != info["sha256"]:
            raise Gagal("File mesin/%s berbeda dari salinan resmi skill %s (versi %s). Hitungan dihentikan agar "
                        "angka tidak salah. Pasang ulang skill gaji-umkm dari paket aslinya."
                        % (nama, info["skill_sumber"], info["versi_skill_sumber"]))
    return manifest


def jalankan_mesin(script, argv):
    cek_mesin()
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run([sys.executable, str(MESIN / script)] + argv, capture_output=True, env=env,
                           timeout=180)
    except subprocess.TimeoutExpired:
        raise Gagal("Mesin hitung %s tidak selesai dalam 3 menit." % script)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    if p.returncode != 0:
        baris = [b.strip() for b in err.splitlines() if b.strip() and not b.startswith("usage")]
        pesan = "\n".join(baris) or "kode keluar %d" % p.returncode
        raise Gagal("Mesin hitung (%s) menolak data:\n%s" % (script, pesan), mesin=script)
    try:
        return json.loads(out)
    except ValueError:
        raise Gagal("Keluaran mesin %s tidak bisa dibaca." % script)


def tulis_csv_mesin(path, kolom, baris):
    """CSV pemisah ';' tanpa koma/titik koma di nilai (agar deteksi pemisah di script sumber selalu ';')."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\n")
        w.writerow(kolom)
        for b in baris:
            w.writerow([re.sub(r"[;,\t\"]", " ", str(b.get(k, "") if b.get(k) is not None else "")) for k in kolom])
    with open(path, encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------------- karyawan
KOLOM_KARYAWAN_TAMPIL = ["kode", "nama", "jabatan", "jenis", "ptkp", "gaji_pokok", "tunjangan_tetap",
                         "tunjangan_tidak_tetap", "bpjs", "jkk_persen", "hari_kerja", "tanggal_masuk",
                         "tanggal_keluar", "nik", "bank", "rekening", "kode_absensi"]


def bpjs_teks(k):
    b = []
    if k["ikut_kes"]:
        b.append("kes")
    if k["ikut_tk"]:
        b.append("tk")
    if k["ikut_jp"]:
        b.append("jp")
    return ",".join(b) or "tidak"


def parse_bpjs(teks):
    s = str(teks or "").strip().lower().replace(" ", "")
    if s in ("semua", "ya", "lengkap", "all"):
        return 1, 1, 1
    if s in ("tidak", "-", "tanpa", "no", "0"):
        return 0, 0, 0
    bag = set(x for x in re.split(r"[,+/]", s) if x)
    alias = {"kesehatan": "kes", "ks": "kes", "ketenagakerjaan": "tk", "bpjstk": "tk", "naker": "tk",
             "pensiun": "jp", "jht": "tk"}
    bag = {alias.get(x, x) for x in bag}
    salah = bag - {"kes", "tk", "jp"}
    if salah:
        raise Gagal("--bpjs: '%s' tidak dikenal. Pakai kombinasi kes,tk,jp (mis. kes,tk,jp atau kes,tk) atau "
                    "'tidak'." % ",".join(sorted(salah)))
    if "jp" in bag and "tk" not in bag:
        raise Gagal("--bpjs: JP (Jaminan Pensiun) hanya bisa bila ikut BPJS Ketenagakerjaan (tk).")
    return int("kes" in bag), int("tk" in bag), int("jp" in bag)


def normalisasi_karyawan(d, lama=None):
    """d: dict opsi (sudah pakai nama kolom db). Kembalikan dict kolom db tervalidasi."""
    o = dict(lama) if lama else {}
    label = d.get("nama") or (lama or {}).get("nama") or "karyawan"
    if "nama" in d:
        o["nama"] = bersih(d["nama"], 80)
        if not o["nama"]:
            raise Gagal("Nama karyawan kosong")
    if "jabatan" in d:
        o["jabatan"] = bersih(d["jabatan"], 60)
    if "jenis" in d and d["jenis"] not in (None, ""):
        j = str(d["jenis"]).strip().lower()
        peta = {"tetap": "tetap", "pkwtt": "tetap", "permanen": "tetap", "kontrak": "kontrak", "pkwt": "kontrak"}
        if j not in peta:
            raise Gagal("%s: jenis harus 'tetap' atau 'kontrak'. Pekerja harian/borongan tidak didukung aplikasi "
                        "bulanan ini (pakai skill pph21-ter/hitung-thr)." % label)
        o["jenis"] = peta[j]
    if "ptkp" in d:
        try:
            o["ptkp"] = tc.normalisasi_ptkp(d["ptkp"])
        except ValueError as e:
            raise Gagal("%s: %s" % (label, e))
    for k in ("gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap", "zakat"):
        if k in d and d[k] not in (None, ""):
            o[k] = teks_angka(uang(d[k], "%s: %s" % (label, k)))
    if "gaji_pokok" in o and D(o["gaji_pokok"]) <= 0:
        raise Gagal("%s: gaji pokok harus lebih dari 0" % label)
    for k in ("dasar_bpjs_kesehatan", "bruto_tetap_januari"):
        if k in d:
            o[k] = "" if d[k] in (None, "", "-") else teks_angka(uang(d[k], "%s: %s" % (label, k)))
    if "bpjs" in d and d["bpjs"] not in (None, ""):
        o["ikut_kes"], o["ikut_tk"], o["ikut_jp"] = parse_bpjs(d["bpjs"])
    if "jkk_persen" in d:
        o["jkk_persen"] = "" if d["jkk_persen"] in (None, "", "-") else teks_angka(
            persen(d["jkk_persen"], "%s: jkk" % label))
    if "hari_kerja" in d and d["hari_kerja"] not in (None, ""):
        if str(d["hari_kerja"]).strip() not in ("5", "6"):
            raise Gagal("%s: pola hari kerja harus 5 atau 6" % label)
        o["hari_kerja"] = int(str(d["hari_kerja"]).strip())
    if "dtp" in d and d["dtp"] not in (None, ""):
        o["dtp"] = int(ya_tidak(d["dtp"], "%s: dtp" % label))
    if "nik" in d:
        try:
            o["nik"] = cek_nik(d["nik"]) if d["nik"] != "-" else ""
        except Gagal as e:
            raise Gagal("%s: %s" % (label, e.pesan))
    if "rekening" in d:
        try:
            o["rekening"] = cek_rekening(d["rekening"]) if d["rekening"] != "-" else ""
        except Gagal as e:
            raise Gagal("%s: %s" % (label, e.pesan))
    for k, m in (("bank", 40), ("atas_nama", 80), ("kode_absensi", 20)):
        if k in d:
            o[k] = "" if d[k] == "-" else bersih(d[k], m)
    if "tanggal_masuk" in d and d["tanggal_masuk"] not in (None, ""):
        o["tanggal_masuk"] = tanggal(d["tanggal_masuk"], "%s: tanggal masuk" % label).isoformat()
    if "tanggal_keluar" in d:
        o["tanggal_keluar"] = "" if d["tanggal_keluar"] in (None, "", "-") else tanggal(
            d["tanggal_keluar"], "%s: tanggal keluar" % label).isoformat()
    for wajib in ("nama", "ptkp", "gaji_pokok", "tanggal_masuk"):
        if not o.get(wajib):
            raise Gagal("%s: %s wajib diisi (%s)." % (label, wajib.replace("_", " "), {
                "nama": "--nama", "ptkp": "--ptkp TK/0..K/3", "gaji_pokok": "--gaji-pokok",
                "tanggal_masuk": "--masuk YYYY-MM-DD (dipakai untuk PPh 21 bulan pertama/akhir & THR)"}[wajib]))
    if o.get("tanggal_keluar") and o["tanggal_keluar"] < o["tanggal_masuk"]:
        raise Gagal("%s: tanggal keluar lebih awal dari tanggal masuk" % label)
    return o


def kode_baru(conn):
    n = conn.execute("SELECT COUNT(*) FROM karyawan").fetchone()[0] + 1
    while conn.execute("SELECT 1 FROM karyawan WHERE kode=?", ("K%03d" % n,)).fetchone():
        n += 1
    return "K%03d" % n


def cari_karyawan(conn, teks):
    s = str(teks or "").strip()
    if not s:
        raise Gagal("Sebutkan karyawannya (--karyawan kode atau nama).")
    r = conn.execute("SELECT * FROM karyawan WHERE lower(kode)=lower(?)", (s,)).fetchall()
    if not r:
        r = conn.execute("SELECT * FROM karyawan WHERE lower(nama)=lower(?)", (s,)).fetchall()
    if not r:
        r = [x for x in conn.execute("SELECT * FROM karyawan ORDER BY kode") if s.lower() in x["nama"].lower()]
    if not r:
        raise Gagal("Karyawan '%s' tidak ditemukan. Lihat: gaji.py karyawan daftar" % s)
    if len(r) > 1:
        pilihan = ["%s (%s%s)" % (x["kode"], x["nama"], ", " + x["jabatan"] if x["jabatan"] else "") for x in r]
        raise Gagal("'%s' cocok dengan %d karyawan: %s. Ulangi dengan kodenya." % (s, len(r), "; ".join(pilihan)),
                    pilihan=[x["kode"] for x in r])
    return r[0]


def ringkas_karyawan(k, samar=True):
    return {
        "kode": k["kode"], "nama": k["nama"], "jabatan": k["jabatan"], "jenis": k["jenis"], "ptkp": k["ptkp"],
        "gaji_pokok": D(k["gaji_pokok"]), "tunjangan_tetap": D(k["tunjangan_tetap"]),
        "tunjangan_tidak_tetap": D(k["tunjangan_tidak_tetap"]), "bpjs": bpjs_teks(k),
        "jkk_persen": k["jkk_persen"] or "(default)", "hari_kerja": k["hari_kerja"],
        "tanggal_masuk": k["tanggal_masuk"], "tanggal_keluar": k["tanggal_keluar"],
        "nik": samarkan(k["nik"]) if samar else k["nik"], "bank": k["bank"],
        "rekening": samarkan(k["rekening"]) if samar else k["rekening"], "kode_absensi": k["kode_absensi"],
    }


def teks_karyawan(k):
    r = ringkas_karyawan(k)
    t = "%s %s%s | %s %s | gaji pokok %s + tunj. tetap %s" % (
        r["kode"], r["nama"], " (%s)" % r["jabatan"] if r["jabatan"] else "", r["jenis"], r["ptkp"],
        rp(r["gaji_pokok"]), rp(r["tunjangan_tetap"]))
    if r["tunjangan_tidak_tetap"]:
        t += " + tunj. tidak tetap rutin %s" % rp(r["tunjangan_tidak_tetap"])
    t += " | BPJS: %s | pola %s hari | masuk %s" % (r["bpjs"], r["hari_kerja"], ftgl(date.fromisoformat(
        r["tanggal_masuk"])))
    if r["tanggal_keluar"]:
        t += " | KELUAR %s" % ftgl(date.fromisoformat(r["tanggal_keluar"]))
    if r["nik"]:
        t += " | NIK %s" % r["nik"]
    if r["rekening"]:
        t += " | %s %s" % (r["bank"] or "rek.", r["rekening"])
    return t


KOLOM_DB = ["kode", "nama", "jabatan", "jenis", "ptkp", "gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap",
            "zakat", "ikut_kes", "ikut_tk", "ikut_jp", "jkk_persen", "hari_kerja", "dasar_bpjs_kesehatan", "dtp",
            "bruto_tetap_januari", "nik", "bank", "rekening", "atas_nama", "kode_absensi", "tanggal_masuk",
            "tanggal_keluar"]
DEFAULT_KARYAWAN = {"jabatan": "", "jenis": "tetap", "tunjangan_tetap": "0", "tunjangan_tidak_tetap": "0",
                    "zakat": "0", "ikut_kes": 1, "ikut_tk": 1, "ikut_jp": 1, "jkk_persen": "", "hari_kerja": 5,
                    "dasar_bpjs_kesehatan": "", "dtp": 0, "bruto_tetap_januari": "", "nik": "", "bank": "",
                    "rekening": "", "atas_nama": "", "kode_absensi": "", "tanggal_keluar": ""}


def simpan_karyawan_baru(conn, o):
    row = dict(DEFAULT_KARYAWAN)
    row.update(o)
    if not row.get("kode"):
        row["kode"] = kode_baru(conn)
    row["kode"] = bersih(row["kode"], 20).upper()
    if not re.fullmatch(r"[A-Z0-9_-]{1,20}", row["kode"]):
        raise Gagal("Kode karyawan hanya huruf/angka/-/_ (mis. K001)")
    if conn.execute("SELECT 1 FROM karyawan WHERE kode=?", (row["kode"],)).fetchone():
        raise Gagal("Kode %s sudah dipakai karyawan lain." % row["kode"])
    if row["nik"] and conn.execute("SELECT kode FROM karyawan WHERE nik=?", (row["nik"],)).fetchone():
        raise Gagal("%s: NIK itu sudah terdaftar pada karyawan lain." % row["nama"])
    w = stempel()
    conn.execute("INSERT INTO karyawan(%s, dibuat, diubah) VALUES (%s)" % (
        ",".join(KOLOM_DB), ",".join("?" * (len(KOLOM_DB) + 2))), [row[k] for k in KOLOM_DB] + [w, w])
    return conn.execute("SELECT * FROM karyawan WHERE kode=?", (row["kode"],)).fetchone()


def opsi_karyawan(args):
    peta = {"nama": "nama", "jabatan": "jabatan", "jenis": "jenis", "ptkp": "ptkp", "gaji_pokok": "gaji_pokok",
            "tunjangan_tetap": "tunjangan_tetap", "tunjangan_tidak_tetap": "tunjangan_tidak_tetap", "zakat": "zakat",
            "bpjs": "bpjs", "jkk": "jkk_persen", "hari_kerja": "hari_kerja",
            "dasar_bpjs_kesehatan": "dasar_bpjs_kesehatan", "dtp": "dtp", "bruto_tetap_januari": "bruto_tetap_januari",
            "nik": "nik", "bank": "bank", "rekening": "rekening", "atas_nama": "atas_nama",
            "kode_absensi": "kode_absensi", "masuk": "tanggal_masuk"}
    return {kol: getattr(args, a) for a, kol in peta.items() if getattr(args, a, None) is not None}


def peringatan_karyawan(o, cfg):
    p = []
    if o.get("dtp"):
        p.append("%s: PPh 21 DTP (PMK 105/2025) hanya untuk masa pajak 2026, sektor/KLU yang tercantum di Lampiran "
                 "PMK 105/2025, dan bruto tetap Januari/bulan pertama kerja <= Rp 10 jt. Pastikan sektor sudah "
                 "dikonfirmasi pemilik." % o["nama"])
    if D(o.get("tunjangan_tetap")) > 0 and D(o["gaji_pokok"]) < (D(o["gaji_pokok"]) + D(o["tunjangan_tetap"])) * \
            Decimal("0.75"):
        p.append("%s: gaji pokok kurang dari 75%% dari (gaji pokok + tunjangan tetap) - cek PP 36/2021 Pasal 7 "
                 "ayat (2)." % o["nama"])
    return p


BATAS_ATAS_KES = Decimal(12000000)      # Perpres 64/2020 Pasal 32 (sama dengan mesin slip-gaji-bpjs)
DASAR_KEPATUHAN = ("UU 24/2011 Pasal 15 ayat (1)-(2): pemberi kerja wajib mendaftarkan dirinya dan pekerjanya ke "
                   "BPJS dan memberikan data yang lengkap dan benar; Perpres 82/2018 jo. 64/2020 Pasal 32: dasar iuran "
                   "BPJS Kesehatan = gaji pokok + tunjangan tetap (maks. Rp 12.000.000, min. UMK); PP 86/2013: sanksi "
                   "teguran, denda, sampai tidak mendapat layanan publik tertentu")
FLAG_PAHAM = "--ya-saya-paham"


def dasar_kes_wajib(o, cfg):
    """Dasar iuran BPJS Kesehatan menurut aturan: min(max(gaji pokok + tunjangan tetap, UMK), 12 jt)."""
    upah = D(o.get("gaji_pokok")) + D(o.get("tunjangan_tetap"))
    if cfg.get("umk"):
        upah = max(upah, D(cfg["umk"]))
    return min(upah, BATAS_ATAS_KES)


def masalah_kepatuhan(o, cfg):
    """Kondisi data karyawan yang tidak sesuai kewajiban BPJS. Kembalikan {kode_masalah: pesan}."""
    nama = o.get("nama") or "karyawan"
    m = {}
    if not int(o.get("ikut_kes") or 0):
        m["tanpa_bpjs_kesehatan"] = ("%s: TIDAK didaftarkan BPJS Kesehatan. Pekerja penerima upah (tetap maupun "
                                     "kontrak) wajib didaftarkan pemberi kerja." % nama)
    if not int(o.get("ikut_tk") or 0):
        m["tanpa_bpjs_ketenagakerjaan"] = ("%s: TIDAK didaftarkan BPJS Ketenagakerjaan (JKK, JKM, JHT). Pekerja "
                                           "penerima upah wajib didaftarkan pemberi kerja." % nama)
    if int(o.get("ikut_kes") or 0) and str(o.get("dasar_bpjs_kesehatan") or "").strip():
        wajib = dasar_kes_wajib(o, cfg)
        if D(o["dasar_bpjs_kesehatan"]) < wajib:
            m["dasar_bpjs_kesehatan_rendah"] = (
                "%s: dasar iuran BPJS Kesehatan diisi %s, lebih kecil dari dasar menurut aturan %s (gaji pokok + "
                "tunjangan tetap, min. UMK bila diisi, maks. Rp 12.000.000). Melaporkan upah lebih kecil dari "
                "sebenarnya tidak dibenarkan." % (nama, rp(D(o["dasar_bpjs_kesehatan"])), rp(wajib)))
    return m


def pagar_kepatuhan(args, baru, langsung_simpan=False):
    """baru: {kode_masalah: pesan} yang MUNCUL karena perintah ini. Tanpa --ya-saya-paham: pratinjau diberi
    peringatan; penyimpanan (--ya) ditolak. Dengan flag: disimpan dan dicatat di log (audit).
    langsung_simpan=True untuk perintah yang menyimpan tanpa --ya (mis. `isi`): tanpa flag selalu ditolak."""
    if not baru:
        return [], None
    pesan = list(baru.values())
    paham = bool(getattr(args, "ya_saya_paham", False))
    if not paham:
        teks = ("PERLU PERSETUJUAN KHUSUS - data ini tidak sesuai kewajiban BPJS:\n- " + "\n- ".join(pesan) +
                "\nDasar: " + DASAR_KEPATUHAN + ". Karyawan juga kehilangan perlindungan (berobat, kecelakaan "
                "kerja, hari tua).\nBila ada alasan sah (mis. iuran sudah dibayar lewat sistem lain, atau sudah "
                "dikonfirmasi ke BPJS), pemilik sendiri harus membaca peringatan ini dan menyetujuinya secara khusus "
                "beserta alasannya. Persetujuan ini dicatat di log aplikasi.")
        if getattr(args, "ya", False) or langsung_simpan:
            raise Gagal("Belum disimpan. " + teks + " (Untuk agent: " + LANGKAH_PERSETUJUAN + ")",
                        masalah_kepatuhan=sorted(baru), langkah_berikut=[LANGKAH_PERSETUJUAN])
        return [teks], None
    catat = {"masalah": sorted(baru), "pesan": pesan, "alasan": bersih(getattr(args, "alasan_khusus", "") or "", 200),
             "waktu": stempel()}
    return ["DISIMPAN DENGAN PERSETUJUAN KHUSUS PEMILIK%s, tercatat di log aplikasi:\n- %s\nRisiko tetap "
            "ditanggung pemberi kerja (%s)." % (" (alasan: %s)" % catat["alasan"] if catat["alasan"] else "",
                                                "\n- ".join(pesan), DASAR_KEPATUHAN)], catat


def bulan_penuh(k, kode):
    """True bila karyawan bekerja sebulan penuh di periode ini (tidak masuk/keluar di tengah bulan)."""
    awal, akhir = rentang_periode(kode)
    masuk_tengah = awal.isoformat() < k["tanggal_masuk"] <= akhir.isoformat()
    keluar_tengah = bool(k["tanggal_keluar"]) and awal.isoformat() <= k["tanggal_keluar"] < akhir.isoformat()
    return not masuk_tengah and not keluar_tengah


def masalah_dasar_turun(k, isi, kode):
    """v1.0.2: gaji pokok/tunjangan tetap 'dibayar' yang menurunkan dasar iuran BPJS di bulan PENUH (bukan bulan
    masuk/keluar). Dasar BPJS = gaji pokok + tunjangan tetap; menurunkannya tanpa dasar sah = melaporkan upah lebih
    kecil. Kembalikan {kode_masalah: pesan} (kosong bila tidak ada masalah)."""
    if not bulan_penuh(k, kode) or not ("gaji_pokok" in isi or "tunjangan_tetap" in isi):
        return {}
    penuh = D(k["gaji_pokok"]) + D(k["tunjangan_tetap"])
    dibayar = D(isi.get("gaji_pokok", k["gaji_pokok"])) + D(isi.get("tunjangan_tetap", k["tunjangan_tetap"]))
    if dibayar >= penuh:
        return {}
    return {"dasar_bpjs_turun_bulan_penuh": (
        "%s: gaji pokok + tunjangan tetap %s diisi %s, di bawah data karyawan %s padahal bekerja sebulan penuh "
        "(bukan bulan masuk/keluar), jadi dasar iuran BPJS Kesehatan & Ketenagakerjaan ikut turun. Bila "
        "gaji memang dipotong karena alasan sah (mis. cuti di luar tanggungan menurut perjanjian kerja), sebutkan "
        "alasannya; bila tujuannya menghemat iuran (mis. bonus dinaikkan, gaji pokok diturunkan), itu tidak "
        "dibenarkan - pakai data gaji penuh." % (k["nama"], nama_periode(kode), rp(dibayar), rp(penuh)))}


def cmd_karyawan_tambah(args):
    def kerja(conn, cfg):
        o = normalisasi_karyawan(opsi_karyawan(args))
        if args.kode:
            o["kode"] = args.kode
        k = simpan_karyawan_baru(conn, o)
        pr_k, catat = pagar_kepatuhan(args, masalah_kepatuhan(dict(k), cfg))
        t = "Karyawan baru:\n- " + teks_karyawan(k)
        ringkasan = {"kode": k["kode"]}
        if catat:
            ringkasan["konfirmasi_kepatuhan"] = catat
        return {"karyawan": ringkas_karyawan(k), "peringatan": pr_k + peringatan_karyawan(dict(k), cfg),
                "perlu_persetujuan_khusus": bool(pr_k) and not catat, "konfirmasi_kepatuhan": catat,
                "ringkasan": ringkasan}, t
    return jalankan_tulis(args, "karyawan tambah", kerja, besar=True, label_backup="karyawan")


def cmd_karyawan_ubah(args):
    def kerja(conn, cfg):
        k = cari_karyawan(conn, args.karyawan)
        d = opsi_karyawan(args)
        if args.keluar is not None:
            d["tanggal_keluar"] = args.keluar
        if not d:
            raise Gagal("Tidak ada yang diubah. Sebutkan opsi, mis. --gaji-pokok 5,5jt atau --ptkp K/1.")
        lama = {c: k[c] for c in KOLOM_DB}
        o = normalisasi_karyawan(d, lama)
        beda = [c for c in KOLOM_DB if str(o.get(c, "")) != str(lama.get(c, ""))]
        if not beda:
            raise Gagal("Data %s sudah sama; tidak ada yang berubah." % k["nama"])
        if "nik" in beda and o["nik"] and conn.execute("SELECT 1 FROM karyawan WHERE nik=? AND id<>?",
                                                       (o["nik"], k["id"])).fetchone():
            raise Gagal("NIK itu sudah terdaftar pada karyawan lain.")
        conn.execute("UPDATE karyawan SET %s, diubah=? WHERE id=?" % ",".join("%s=?" % c for c in beda),
                     [o[c] for c in beda] + [stempel(), k["id"]])
        k2 = conn.execute("SELECT * FROM karyawan WHERE id=?", (k["id"],)).fetchone()
        lama_m = masalah_kepatuhan(lama, cfg)
        baru_m = {kd: ps for kd, ps in masalah_kepatuhan(dict(k2), cfg).items() if kd not in lama_m}
        pr_k, catat = pagar_kepatuhan(args, baru_m)
        rahasia = {"nik", "rekening"}
        baris = ["- %s: %s -> %s" % (c.replace("_", " "),
                                     samarkan(lama[c]) if c in rahasia else (lama[c] or "(kosong)"),
                                     samarkan(o[c]) if c in rahasia else (o[c] or "(kosong)")) for c in beda]
        t = "Ubah data %s (%s):\n%s" % (k["nama"], k["kode"], "\n".join(baris))
        pr = pr_k + (peringatan_karyawan(dict(k2), cfg) if ("dtp" in beda or "gaji_pokok" in beda) else [])
        draf = [r["kode"] for r in conn.execute("SELECT kode FROM periode WHERE status='draf' ORDER BY kode")]
        langkah = []
        if draf:
            pr.append("Gaji %s (draf) masih memakai data lama sampai dihitung ulang." % ", ".join(
                nama_periode(x) for x in draf))
            langkah += ["hitung --bulan %s" % x for x in draf]
        final = [r["kode"] for r in conn.execute("SELECT kode FROM periode WHERE status='final' ORDER BY kode")]
        if final:
            pr.append("Gaji yang sudah dikunci (%s) TIDAK berubah. Bila perubahan ini juga berlaku untuk bulan yang "
                      "sudah dikunci, bulan itu perlu direvisi (dengan alasan tercatat)." % ", ".join(
                          nama_periode(x) for x in final))
            langkah.append("Bila pemilik minta bulan final ikut berubah: revisi --bulan <periode> --alasan \"...\"")
        if "tanggal_keluar" in beda and o["tanggal_keluar"]:
            kp = o["tanggal_keluar"][:7]
            pr.append("%s keluar %s: %s menjadi Masa Pajak Terakhir (PPh 21 dihitung ulang setahun, butuh gaji bulan "
                      "sebelumnya tahun ini sudah dikunci atau saldo awal). Gaji bulan itu tetap penuh kecuali Anda "
                      "menyebut gaji yang dibayar (mis. prorata)." % (
                          k["nama"], ftgl(date.fromisoformat(o["tanggal_keluar"])), nama_periode(kp)))
            langkah.append("Gaji dibayar bulan keluar: isi --bulan %s --karyawan %s --gaji-pokok-dibayar .. atau hitung "
                           "--bulan %s --prorata kalender" % (kp, k["kode"], kp))
        ringkasan = {"kode": k["kode"], "kolom": beda}
        if catat:
            ringkasan["konfirmasi_kepatuhan"] = catat
        return {"karyawan": ringkas_karyawan(k2), "berubah": beda, "peringatan": pr, "langkah_berikut": langkah,
                "perlu_persetujuan_khusus": bool(pr_k) and not catat, "konfirmasi_kepatuhan": catat,
                "ringkasan": ringkasan}, t
    return jalankan_tulis(args, "karyawan ubah", kerja, besar=True, label_backup="karyawan")


def cmd_karyawan_daftar(args):
    def kerja(conn, cfg):
        rows = conn.execute("SELECT * FROM karyawan ORDER BY kode").fetchall()
        aktif = [k for k in rows if not k["tanggal_keluar"] or k["tanggal_keluar"] >= hari_ini().isoformat()]
        if not args.semua:
            rows = aktif
        if not rows:
            return {"karyawan": []}, "Belum ada karyawan. Tambah: gaji.py karyawan tambah --nama ... (atau karyawan impor)."
        t = "Daftar karyawan (%d%s):\n" % (len(rows), "" if args.semua else " aktif") + "\n".join(
            "- " + teks_karyawan(k) for k in rows)
        t += "\n(NIK & nomor rekening selalu disamarkan.)"
        return {"karyawan": [ringkas_karyawan(k) for k in rows]}, t
    return baca(args, kerja)


def baca_tabel(path):
    try:
        mentah = Path(path).expanduser().read_bytes()
    except OSError as e:
        raise Gagal("File '%s' tidak bisa dibaca: %s" % (path, e.strerror))
    if mentah[:4] == b"PK\x03\x04":
        raise Gagal("File itu Excel (.xlsx). Simpan dulu sebagai CSV (File > Save As > CSV) lalu ulangi.")
    teks = None
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            teks = mentah.decode(enc)
            if "\x00" in teks:
                continue
            break
        except UnicodeDecodeError:
            continue
    if not teks or not teks.strip():
        raise Gagal("File '%s' kosong." % path)
    baris1 = teks.splitlines()[0]
    pemisah = max([";", ",", "\t", "|"], key=lambda c: baris1.count(c))
    rd = csv.reader(io.StringIO(teks), delimiter=pemisah)
    tabel = [r for r in rd if any((c or "").strip() for c in r)]
    if len(tabel) < 2:
        raise Gagal("File '%s' tidak berisi data (hanya judul/kosong)." % path)
    kepala = [re.sub(r"[^a-z0-9_]", "", c.strip().lower().replace(" ", "_").replace("-", "_")) for c in tabel[0]]
    hasil = []
    for i, r in enumerate(tabel[1:], start=2):
        r = list(r) + [""] * (len(kepala) - len(r))
        d = {kepala[j]: (r[j] or "").strip() for j in range(len(kepala)) if kepala[j]}
        d["_baris"] = i
        hasil.append(d)
    return kepala, hasil


ALIAS_IMPOR = {"nama_karyawan": "nama", "status_ptkp": "ptkp", "gaji": "gaji_pokok", "upah_pokok": "gaji_pokok",
               "tunjangan": "tunjangan_tetap", "posisi": "jabatan", "tanggal_mulai": "masuk",
               "tanggal_masuk": "masuk", "mulai": "masuk", "no_rekening": "rekening", "nomor_rekening": "rekening",
               "jkk_persen": "jkk", "pola_hari_kerja": "hari_kerja", "tanggal_keluar": "keluar"}


def impor_baris_karyawan(conn, cfg, rows, masuk_default=None):
    """Simpan baris CSV karyawan ke conn. Kembalikan (baru, peringatan, masalah_kepatuhan, galat, tanpa_masuk).
    masuk_default (hitung-cepat): tanggal masuk dipakai bila kolom masuk kosong (nama dicatat di tanpa_masuk)."""
    galat, baru, pr, masalah, tanpa_masuk = [], [], [], {}, []
    for r in rows:
        r = {ALIAS_IMPOR.get(k, k): v for k, v in r.items()}
        d = {k: r[k] for k in ("nama", "jabatan", "jenis", "ptkp", "gaji_pokok", "tunjangan_tetap",
                               "tunjangan_tidak_tetap", "zakat", "bpjs", "hari_kerja", "dtp",
                               "bruto_tetap_januari", "nik", "bank", "rekening", "atas_nama", "kode_absensi",
                               "dasar_bpjs_kesehatan") if r.get(k) not in (None, "")}
        if r.get("jkk"):
            d["jkk_persen"] = r["jkk"]
        if r.get("masuk"):
            d["tanggal_masuk"] = r["masuk"]
        elif masuk_default:
            d["tanggal_masuk"] = masuk_default
            tanpa_masuk.append(bersih(r.get("nama") or "baris %d" % r["_baris"], 80))
        if r.get("keluar"):
            d["tanggal_keluar"] = r["keluar"]
        try:
            o = normalisasi_karyawan(d)
            if r.get("kode"):
                o["kode"] = r["kode"]
            k = simpan_karyawan_baru(conn, o)
            baru.append(k)
            pr += peringatan_karyawan(dict(k), cfg)
            for kd, ps in masalah_kepatuhan(dict(k), cfg).items():
                masalah["%s:%s" % (k["kode"], kd)] = "baris %d, %s" % (r["_baris"], ps)
        except Gagal as e:
            galat.append("baris %d: %s" % (r["_baris"], e.pesan))
    return baru, pr, masalah, galat, tanpa_masuk


def cmd_karyawan_impor(args):
    def kerja(conn, cfg):
        kepala, rows = baca_tabel(args.file)
        kepala = [ALIAS_IMPOR.get(k, k) for k in kepala]
        if not {"nama", "ptkp", "gaji_pokok", "masuk"} <= set(kepala):
            raise Gagal("File wajib punya kolom nama, ptkp, gaji_pokok, masuk (tanggal masuk). Contoh: "
                        "templates/karyawan-contoh.csv. Kolom ditemukan: %s" % ", ".join(kepala))
        baru, pr, masalah, galat, _ = impor_baris_karyawan(conn, cfg, rows)
        if galat:
            raise Gagal("Tidak ada yang disimpan; perbaiki dulu:\n- " + "\n- ".join(galat), galat=galat)
        pr_k, catat = pagar_kepatuhan(args, masalah)
        t = "Impor %d karyawan:\n%s" % (len(baru), "\n".join("- " + teks_karyawan(k) for k in baru))
        ringkasan = {"jumlah": len(baru)}
        if catat:
            ringkasan["konfirmasi_kepatuhan"] = catat
        return {"jumlah": len(baru), "karyawan": [ringkas_karyawan(k) for k in baru], "peringatan": pr_k + pr,
                "perlu_persetujuan_khusus": bool(pr_k) and not catat, "konfirmasi_kepatuhan": catat,
                "ringkasan": ringkasan}, t
    return jalankan_tulis(args, "karyawan impor", kerja, besar=True, label_backup="impor")


# --------------------------------------------------------------------------- periode & isian
def ambil_periode(conn, kode, buat=False):
    r = conn.execute("SELECT * FROM periode WHERE kode=?", (kode,)).fetchone()
    if r or not buat:
        return r
    conn.execute("INSERT INTO periode(kode, status, revisi, dibuat) VALUES (?, 'draf', 0, ?)", (kode, stempel()))
    return conn.execute("SELECT * FROM periode WHERE kode=?", (kode,)).fetchone()


def wajib_draf(per):
    if per["status"] == "final":
        raise Gagal("Periode %s sudah FINAL (terkunci). Perubahan wajib lewat revisi tercatat: gaji.py revisi --bulan "
                    "%s --alasan \"...\" (pratinjau, lalu --ya)." % (nama_periode(per["kode"]), per["kode"]),
                    terkunci=True)


def karyawan_periode(conn, kode):
    awal, akhir = rentang_periode(kode)
    return [k for k in conn.execute("SELECT * FROM karyawan ORDER BY kode")
            if k["tanggal_masuk"] <= akhir.isoformat() and (not k["tanggal_keluar"] or
                                                           k["tanggal_keluar"] >= awal.isoformat())]


def nilai_isian(kolom, nilai, label):
    jenis = ISIAN[kolom][0]
    s = str(nilai).strip()
    if jenis == "uang":
        return teks_angka(uang(s, "%s: %s" % (label, kolom)))
    if jenis == "info":
        try:
            d = tc.parse_angka(s, "%s: %s" % (label, kolom))
        except ValueError as e:
            raise Gagal(str(e))
        return teks_angka(d)
    if jenis == "jam":
        bag = [b for b in re.split(r"[+;/|\s]+", s.replace(",", ".")) if b]
        if not bag:
            raise Gagal("%s: %s kosong" % (label, kolom))
        for b in bag:
            inti = b[:-1] if b.lower().endswith("p") else b
            try:
                j = tc.parse_angka(inti, kolom)
            except ValueError:
                raise Gagal("%s: %s '%s' bukan jam. Tulis jam per hari dipisah +, mis. 2+3+1,5" % (label, kolom, b))
            if j <= 0 or j > 24:
                raise Gagal("%s: %s '%s' harus lebih dari 0 dan tidak lebih dari 24 jam" % (label, kolom, b))
            if b.lower().endswith("p") and kolom != "lembur_hari_libur":
                raise Gagal("%s: akhiran 'p' hanya untuk lembur hari libur" % label)
        return "+".join(bag)
    return bersih(s, 200)


def set_isian(conn, per, k, kolom, nilai, ket=""):
    if nilai in (None,):
        return
    if str(nilai).strip() in ("-", ""):
        conn.execute("DELETE FROM isian WHERE periode_id=? AND karyawan_id=? AND kolom=?", (per["id"], k["id"], kolom))
        return
    v = nilai_isian(kolom, nilai, k["nama"])
    conn.execute("INSERT OR REPLACE INTO isian(periode_id, karyawan_id, kolom, nilai, keterangan) VALUES (?,?,?,?,?)",
                 (per["id"], k["id"], kolom, v, bersih(ket, 200)))


def isian_karyawan(conn, per, k):
    return {r["kolom"]: r["nilai"] for r in conn.execute(
        "SELECT kolom, nilai FROM isian WHERE periode_id=? AND karyawan_id=?", (per["id"], k["id"]))}


def teks_isian(isi):
    if not isi:
        return "(tidak ada komponen tidak tetap)"
    b = []
    for kol, v in isi.items():
        jenis = ISIAN[kol][0]
        b.append("%s %s" % (kol.replace("_", " "), rp(v) if jenis == "uang" else v))
    return ", ".join(b)


def cmd_isi(args):
    kode = parse_periode(args.bulan)
    if args.file:
        return cmd_isi_file(args, kode)
    nilai = {kol: getattr(args, kol) for kol in ISIAN if getattr(args, kol, None) is not None}
    if args.kasbon is not None:
        if "potongan_lain" in nilai:
            raise Gagal("Isi --kasbon ATAU --potongan-lain, jangan keduanya.")
        nilai["potongan_lain"] = args.kasbon
    if args.gaji_pokok_dibayar is not None:
        nilai["gaji_pokok"] = args.gaji_pokok_dibayar
    if args.tunjangan_tetap_dibayar is not None:
        nilai["tunjangan_tetap"] = args.tunjangan_tetap_dibayar
    if not nilai:
        raise Gagal("Sebutkan komponennya, mis. --bonus 500rb --kasbon 200rb --lembur-hari-kerja 2+3.")

    def kerja(conn, cfg):
        per = ambil_periode(conn, kode, buat=True)
        wajib_draf(per)
        k = cari_karyawan(conn, args.karyawan)
        if k["id"] not in [x["id"] for x in karyawan_periode(conn, kode)]:
            raise Gagal("%s tidak aktif di %s (masuk %s%s)." % (k["nama"], nama_periode(kode), k["tanggal_masuk"],
                                                              ", keluar " + k["tanggal_keluar"] if k["tanggal_keluar"]
                                                              else ""))
        pr = []
        if "potongan_tidak_masuk" in nilai and str(nilai["potongan_tidak_masuk"]).strip() not in ("-", "0", ""):
            pr.append("Potongan tidak masuk hanya sah bila diatur di Perjanjian Kerja/Peraturan Perusahaan/PKB "
                      "(PP 36/2021). PPh 21 tetap dihitung dari penghasilan sebelum potongan ini (cara slip-gaji-bpjs); "
                      "bila perusahaan memperlakukannya sebagai pengurang upah, tanyakan ke konsultan pajak.")
        if "gaji_pokok" in nilai or "tunjangan_tetap" in nilai:
            pr.append("Gaji pokok/tunjangan tetap bulan ini diganti nominal yang Anda isi. Dasar iuran BPJS dan upah "
                      "lembur bulan ini ikut memakai angka itu (cara slip-gaji-bpjs). Pastikan sesuai perjanjian kerja; "
                      "cek ke BPJS bila iuran bulan masuk/keluar harus penuh.")
        for kol, v in nilai.items():
            set_isian(conn, per, k, kol, v, args.keterangan or "")
        isi = isian_karyawan(conn, per, k)
        if "lembur_rp" in isi and ("lembur_hari_kerja" in isi or "lembur_hari_libur" in isi):
            raise Gagal("Isi jam lembur ATAU lembur_rp, jangan keduanya (hapus yang satu dengan nilai '-').")
        pr_k, catat = [], None
        if "gaji_pokok" in nilai or "tunjangan_tetap" in nilai:
            pr_k, catat = pagar_kepatuhan(args, masalah_dasar_turun(k, isi, kode), langsung_simpan=True)
        t = "Tersimpan untuk %s, %s (belum dihitung): %s" % (k["nama"], nama_periode(kode), teks_isian(isi))
        ringkasan = {"periode": kode, "karyawan": k["kode"], "kolom": sorted(nilai)}
        if catat:
            ringkasan["konfirmasi_kepatuhan"] = catat
        return {"karyawan": k["kode"], "periode": kode, "isian": isi, "peringatan": pr_k + pr,
                "perlu_persetujuan_khusus": bool(pr_k) and not catat, "konfirmasi_kepatuhan": catat,
                "langkah_berikut": ["hitung --bulan %s" % kode], "ringkasan": ringkasan}, t
    return jalankan_tulis(args, "isi", kerja)


ALIAS_KOMPONEN = {"gaji_pokok_dibayar": "gaji_pokok", "tunjangan_tetap_dibayar": "tunjangan_tetap"}
KOLOM_ABAIKAN = {"kode", "nama", "no", "nomor", "jabatan"}      # bukan komponen, sengaja tidak dipakai


def isi_dari_tabel(conn, per, path):
    """isi --file / hitung-cepat --komponen: komponen banyak karyawan dari CSV. Kembalikan (ok, masalah, galat, asing);
    asing = judul kolom yang tidak dikenal (tidak dipakai) supaya bisa disampaikan, bukan diam-diam diabaikan."""
    kode = per["kode"]
    kepala, rows = baca_tabel(path)
    kepala = [ALIAS_KOMPONEN.get(c, c) for c in kepala]
    rows = [{ALIAS_KOMPONEN.get(c, c): v for c, v in r.items()} for r in rows]
    asing = [c for c in kepala if c and c not in ISIAN and c != "kasbon" and c not in KOLOM_ABAIKAN]
    kolom = [c for c in kepala if c in ISIAN or c == "kasbon"]
    if not ({"kode", "nama"} & set(kepala)) or not kolom:
        raise Gagal("File wajib punya kolom kode atau nama, dan minimal satu komponen (%s)." %
                    ", ".join(sorted(ISIAN)))
    galat, ok, masalah = [], [], {}
    aktif = {k["id"] for k in karyawan_periode(conn, kode)}
    for r in rows:
        try:
            k = cari_karyawan(conn, r.get("kode") or r.get("nama"))
            if k["id"] not in aktif:
                raise Gagal("%s tidak aktif di %s" % (k["nama"], nama_periode(kode)))
            diisi = [c for c in kolom if r.get(c, "") != ""]
            for c in diisi:
                set_isian(conn, per, k, "potongan_lain" if c == "kasbon" else c, r[c])
            isi_k = isian_karyawan(conn, per, k)
            if "lembur_rp" in isi_k and ("lembur_hari_kerja" in isi_k or "lembur_hari_libur" in isi_k):
                raise Gagal("%s: isi jam lembur ATAU lembur_rp, jangan keduanya" % k["nama"])
            if {"gaji_pokok", "tunjangan_tetap"} & set(diisi):
                for kd, ps in masalah_dasar_turun(k, isi_k, kode).items():
                    masalah["%s:%s" % (kd, k["kode"])] = ps
            ok.append((k, isi_k))
        except Gagal as e:
            galat.append("baris %d: %s" % (r["_baris"], e.pesan))
    return ok, masalah, galat, asing


def teks_kolom_asing(asing):
    """Kalimat awam untuk judul kolom komponen yang tidak dikenal (tanpa garis bawah/nama teknis)."""
    nama = ['"%s"' % c.replace("_", " ") for c in asing]
    daftar = nama[0] if len(nama) == 1 else "%s dan %s" % (", ".join(nama[:-1]), nama[-1])
    return ("Isian %s di daftar komponen tidak dikenali, jadi TIDAK dihitung. Bila itu bagian gaji, sebutkan masuk "
            "tunjangan tidak tetap (mis. uang makan/transport), bonus, lembur, kasbon, atau gaji pokok yang dibayar."
            % daftar)


def cmd_isi_file(args, kode):
    def kerja(conn, cfg):
        per = ambil_periode(conn, kode, buat=True)
        wajib_draf(per)
        ok, masalah, galat, asing = isi_dari_tabel(conn, per, args.file)
        if galat:
            raise Gagal("Tidak ada yang disimpan; perbaiki dulu:\n- " + "\n- ".join(galat), galat=galat)
        pr_k, catat = pagar_kepatuhan(args, masalah)       # HANYA masalah kepatuhan BPJS (pagar persetujuan)
        t = "Komponen %s:\n%s" % (nama_periode(kode), "\n".join("- %s: %s" % (k["nama"], teks_isian(i)) for k, i in ok))
        ringkasan = {"periode": kode, "jumlah": len(ok)}
        if catat:
            ringkasan["konfirmasi_kepatuhan"] = catat
        # kolom asing: catatan biasa untuk pemilik (bahasa awam) + daftar teknis di JSON; tidak pernah memicu
        # perlu_persetujuan_khusus (bukan masalah kepatuhan)
        return {"periode": kode, "jumlah": len(ok), "peringatan": pr_k + ([teks_kolom_asing(asing)] if asing else []),
                "kolom_tidak_dikenal": asing, "kolom_dikenal": sorted(set(ISIAN) | {"kasbon"} | set(ALIAS_KOMPONEN)),
                "perlu_persetujuan_khusus": bool(pr_k) and not catat, "konfirmasi_kepatuhan": catat,
                "ringkasan": ringkasan}, t
    return jalankan_tulis(args, "isi --file", kerja, besar=True, label_backup="isian")


def cmd_impor_absensi(args):
    kode = parse_periode(args.bulan)

    def kerja(conn, cfg):
        per = ambil_periode(conn, kode, buat=True)
        wajib_draf(per)
        kepala, rows = baca_tabel(args.file)
        if "nama" not in kepala and "kode_absensi" not in kepala:
            raise Gagal("File bukan rekap absensi-lokal (tidak ada kolom nama/kode_absensi). Buat dengan skill "
                        "absensi-lokal: absensi.py rekap --bulan %s --csv-gaji lembur-gaji.csv" % kode)
        if not {"lembur_hari_kerja", "lembur_hari_libur", "hari_alpa"} & set(kepala):
            raise Gagal("File tidak berisi kolom lembur_hari_kerja/lembur_hari_libur/hari_alpa dari absensi-lokal.")
        tarif = D(cfg["potongan_per_hari_alpa"]) if cfg["potongan_per_hari_alpa"] else None
        aktif = {k["id"]: k for k in karyawan_periode(conn, kode)}
        semua = conn.execute("SELECT * FROM karyawan").fetchall()
        galat, baris, pr = [], [], []
        for r in rows:
            k = None
            ka = (r.get("kode_absensi") or "").strip().lower()
            if ka:
                cocok = [x for x in semua if x["kode_absensi"] and x["kode_absensi"].lower() == ka]
                k = cocok[0] if len(cocok) == 1 else None
            if k is None:
                cocok = [x for x in semua if x["nama"].lower() == (r.get("nama") or "").strip().lower()]
                if len(cocok) > 1:
                    galat.append("baris %d: nama '%s' kembar; isi kode_absensi karyawan (gaji.py karyawan ubah "
                                 "--kode-absensi)" % (r["_baris"], r.get("nama")))
                    continue
                k = cocok[0] if cocok else None
            if k is None:
                galat.append("baris %d: '%s' tidak ada di data gaji. Tambah dulu karyawannya, atau isi kode_absensi "
                             "yang sama." % (r["_baris"], r.get("nama") or r.get("kode_absensi")))
                continue
            if k["id"] not in aktif:
                galat.append("baris %d: %s tidak aktif di %s" % (r["_baris"], k["nama"], nama_periode(kode)))
                continue
            try:
                ada = isian_karyawan(conn, per, k)
                lk, ll = r.get("lembur_hari_kerja", ""), r.get("lembur_hari_libur", "")
                if (lk or ll) and "lembur_rp" in ada:
                    pr.append("%s: sudah ada lembur nominal %s; jam lembur dari absensi TIDAK dimasukkan agar tidak "
                              "dobel. Hapus salah satu." % (k["nama"], rp(ada["lembur_rp"])))
                else:
                    set_isian(conn, per, k, "lembur_hari_kerja", lk or "-", "absensi-lokal")
                    set_isian(conn, per, k, "lembur_hari_libur", ll or "-", "absensi-lokal")
                for c in ("hari_hadir", "hari_alpa", "terlambat_menit"):
                    if r.get(c, "") != "":
                        set_isian(conn, per, k, c, r[c], "absensi-lokal")
                alpa = D(r.get("hari_alpa") or 0)
                pot = None
                if alpa > 0 and tarif:
                    pot = tc.bulat_terdekat(alpa * tarif)
                    set_isian(conn, per, k, "potongan_tidak_masuk", teks_angka(pot),
                              "%s hari x %s (%s)" % (teks_angka(alpa), rp(tarif), cfg["dasar_potongan"]))
                elif alpa > 0:
                    pr.append("%s: %s hari alpa TIDAK dipotong otomatis (aturan potongan belum diatur). Bila PK/PP/PKB "
                              "mengaturnya: gaji.py atur --potongan-per-hari-alpa <nominal> --dasar-potongan \"<pasal>\", "
                              "lalu impor ulang." % (k["nama"], teks_angka(alpa)))
                gp = r.get("gaji_pokok", "")
                if gp:
                    try:
                        if tc.bulat_terdekat(tc.parse_angka(gp, "gaji_pokok")) != D(k["gaji_pokok"]):
                            pr.append("%s: gaji pokok di file absensi (%s) berbeda dengan data gaji (%s). Rupiah lembur "
                                      "dihitung ulang dari data gaji." % (k["nama"], rp(tc.parse_angka(gp, "x")),
                                                                         rp(k["gaji_pokok"])))
                    except ValueError:
                        pass
                baris.append("- %s: lembur hari kerja %s | hari libur %s | hadir %s, alpa %s%s" % (
                    k["nama"], lk or "-", ll or "-", r.get("hari_hadir") or "-", r.get("hari_alpa") or "0",
                    " -> potongan tidak masuk %s" % rp(pot) if pot else ""))
            except Gagal as e:
                galat.append("baris %d: %s" % (r["_baris"], e.pesan))
        if galat:
            raise Gagal("Tidak ada yang disimpan; perbaiki dulu:\n- " + "\n- ".join(galat), galat=galat)
        tidak_ada = [k["nama"] for i, k in aktif.items() if k["nama"] not in " ".join(baris)]
        if tidak_ada:
            pr.append("Tidak ada di file absensi: %s (komponen lemburnya tidak diubah)." % ", ".join(tidak_ada))
        if tarif:
            pr.append("Potongan tidak masuk %s/hari alpa memakai aturan: %s. Hanya sah bila tercantum di PK/PP/PKB."
                      % (rp(tarif), cfg["dasar_potongan"]))
        t = "Impor rekap absensi %s (%d karyawan):\n%s" % (nama_periode(kode), len(baris), "\n".join(baris))
        return {"periode": kode, "jumlah": len(baris), "peringatan": pr,
                "ringkasan": {"periode": kode, "jumlah": len(baris)}}, t
    return jalankan_tulis(args, "impor-absensi", kerja, besar=True, label_backup="absensi")


def cmd_saldo_awal(args):
    def kerja(conn, cfg):
        k = cari_karyawan(conn, args.karyawan)
        th = int(args.tahun)
        sb = int(args.sampai_bulan)
        if not 1 <= sb <= 11:
            raise Gagal("--sampai-bulan harus 1-11 (bulan terakhir sebelum memakai aplikasi ini).")
        if args.hapus:
            conn.execute("DELETE FROM saldo_awal WHERE karyawan_id=? AND tahun=?", (k["id"], th))
            return {"ringkasan": {"hapus": k["kode"]}}, "Saldo awal %s tahun %d dihapus." % (k["nama"], th)
        vals = [teks_angka(uang(getattr(args, n) or "0", "--" + n)) for n in ("bruto", "pph21", "iuran", "zakat")]
        conn.execute("INSERT OR REPLACE INTO saldo_awal(karyawan_id, tahun, sampai_bulan, bruto, pph21, iuran, zakat) "
                     "VALUES (?,?,?,?,?,?,?)", [k["id"], th, sb] + vals)
        t = ("Saldo awal %s tahun %d (Januari/bulan masuk s.d. %s): bruto pajak %s, PPh 21 dipotong %s, iuran JHT+JP "
             "karyawan %s, zakat %s. Dipakai saat hitung ulang Desember/bulan keluar." % (
                 k["nama"], th, tc.NAMA_BULAN[sb - 1], rp(vals[0]), rp(vals[1]), rp(vals[2]), rp(vals[3])))
        pr = []
        if D(vals[0]) > 0 and not args.iuran and k["ikut_tk"]:
            pr.append("Iuran JHT 2% + JP 1% karyawan belum diisi (dianggap 0) - PPh 21 akhir tahun bisa terlalu besar.")
        return {"peringatan": pr, "ringkasan": {"kode": k["kode"], "tahun": th}}, t
    return jalankan_tulis(args, "saldo-awal", kerja)


# --------------------------------------------------------------------------- hitung
def riwayat_tahun(conn, k, kode):
    """Data Januari (atau bulan masuk) s.d. bulan lalu untuk Masa Pajak Terakhir, dari periode FINAL + saldo awal."""
    th, bl = int(kode[:4]), int(kode[5:7])
    masuk = date.fromisoformat(k["tanggal_masuk"])
    bulan_mulai = masuk.month if masuk.year == th else 1
    tot = {"bruto": NOL, "pph": NOL, "iuran": NOL, "zakat": NOL}
    mulai_cari = bulan_mulai
    sa = conn.execute("SELECT * FROM saldo_awal WHERE karyawan_id=? AND tahun=?", (k["id"], th)).fetchone()
    sumber = []
    if sa:
        if sa["sampai_bulan"] >= bl:
            raise Gagal("%s: saldo awal %d sampai bulan %d, padahal periode ini %s. Perbaiki saldo awal." % (
                k["nama"], th, sa["sampai_bulan"], nama_periode(kode)), saldo_awal_salah=True,
                bulan_mulai=bulan_mulai)
        tot["bruto"] += D(sa["bruto"])
        tot["pph"] += D(sa["pph21"])
        tot["iuran"] += D(sa["iuran"])
        tot["zakat"] += D(sa["zakat"])
        mulai_cari = max(bulan_mulai, sa["sampai_bulan"] + 1)
        sumber.append("saldo awal s.d. %s" % tc.NAMA_BULAN[sa["sampai_bulan"] - 1])
    kurang, bulan_kurang = [], []
    for b in range(mulai_cari, bl):
        kp = "%04d-%02d" % (th, b)
        per = conn.execute("SELECT * FROM periode WHERE kode=?", (kp,)).fetchone()
        if not per or per["status"] != "final":
            jenis = "belum ada" if not per else "belum final" if per["revisi"] == 0 else "sedang direvisi"
            kurang.append("%s (%s)" % (nama_periode(kp), jenis))
            bulan_kurang.append([b, jenis])
            continue
        h = conn.execute("SELECT data FROM hasil WHERE periode_id=? AND revisi=? AND karyawan_id=?",
                         (per["id"], per["revisi"], k["id"])).fetchone()
        if not h:
            kurang.append("%s (tidak ada data %s)" % (nama_periode(kp), k["nama"]))
            bulan_kurang.append([b, "belum ada"])
            continue
        p = json.loads(h["data"])["payroll"]
        tot["bruto"] += D(p["pph_info"]["bruto"])
        tot["pph"] += D(p["pph"])
        tot["iuran"] += D(p["iuran"]["jht_karyawan"]) + D(p["iuran"]["jp_karyawan"])
        tot["zakat"] += D(p["potongan"]["Zakat"])
        sumber.append(kp)
    if kurang:
        raise Gagal("%s: %s adalah Masa Pajak Terakhir, jadi PPh 21 dihitung ulang setahun dan butuh data %s s.d. "
                    "bulan lalu. Belum lengkap: %s. Finalkan periode itu, atau isi saldo awal (gaji.py saldo-awal "
                    "--karyawan %s --tahun %d --sampai-bulan <bulan> --bruto ... --pph21 ... --iuran ...) bila bulan itu "
                    "tidak dihitung di aplikasi ini." % (k["nama"], nama_periode(kode), tc.NAMA_BULAN[bulan_mulai - 1],
                                                          "; ".join(kurang), k["kode"], th), kurang=kurang,
                    bulan_kurang=bulan_kurang, bulan_mulai=bulan_mulai,
                    bulan_pertama_aplikasi=bulan_pertama_aplikasi(conn, th, bl, sa["sampai_bulan"] if sa else None),
                    bulan_periode_pertama=bulan_pertama_aplikasi(conn, th, bl))
    return bulan_mulai, tot, sumber


# --------------------------------------------------------------------------- v1.0.13: tertunda, PPh sementara, prorata
def bulan_pertama_aplikasi(conn, th, bl, saldo_sampai=None):
    """Bulan pertama tahun th yang punya periode di aplikasi (draf/final). Bulan sebelum ini = sebelum aplikasi dipakai
    (datanya hanya bisa lewat saldo awal); bulan sejak ini yang belum ada = terlewat (bisa dihitung & dikunci).
    saldo_sampai: saldo awal karyawan ini sudah mencakup s.d. bulan itu, jadi aplikasi dianggap dipakai sejak bulan
    berikutnya (mis. saldo s.d. Agustus, periode pertama Oktober -> September terlewat: hitung & kunci, atau saldo awal)."""
    r = conn.execute("SELECT MIN(kode) FROM periode WHERE kode LIKE ?", ("%04d-%%" % th,)).fetchone()[0]
    pertama = int(r[5:7]) if r else bl
    return min(pertama, saldo_sampai + 1) if saldo_sampai else pertama


def rentang_bulan(th, b1, b2):
    a, z = tc.NAMA_BULAN[b1 - 1], tc.NAMA_BULAN[b2 - 1]
    return ("%s %d" % (a, th)) if b1 == b2 else ("%s–%s %d" % (a, z, th))


def hari_dibayar(k, kode):
    """(hari kalender bekerja, hari dalam bulan) bila masuk/keluar di tengah bulan; None bila sebulan penuh."""
    if bulan_penuh(k, kode):
        return None
    awal, akhir = rentang_periode(kode)
    mulai = max(awal, date.fromisoformat(k["tanggal_masuk"]))
    selesai = min(akhir, date.fromisoformat(k["tanggal_keluar"])) if k["tanggal_keluar"] else akhir
    return (selesai - mulai).days + 1, (akhir - awal).days + 1


def saran_prorata(k, kode):
    """Prorata HARI KALENDER (pilihan, bukan aturan): nominal x hari bekerja / hari dalam bulan, dibulatkan ke rupiah
    terdekat per komponen. Kembalikan dict atau None bila sebulan penuh."""
    h = hari_dibayar(k, kode)
    if not h:
        return None
    hari, n = h
    gp, tt = D(k["gaji_pokok"]), D(k["tunjangan_tetap"])
    gp_p, tt_p = tc.bulat_terdekat(gp * hari / n), tc.bulat_terdekat(tt * hari / n)
    rumus = "gaji pokok %s × %d ÷ %d hari = %s" % (rp(gp), hari, n, rp(gp_p))
    if tt:
        rumus += "; tunjangan tetap %s × %d ÷ %d = %s" % (rp(tt), hari, n, rp(tt_p))
    return {"kode": k["kode"], "nama": k["nama"], "hari": hari, "hari_bulan": n, "gaji_pokok": gp,
            "tunjangan_tetap": tt, "gaji_pokok_prorata": gp_p, "tunjangan_tetap_prorata": tt_p, "rumus": rumus}


KET_PRORATA = "prorata hari kalender (otomatis)"


def catatan_iuran_prorata(cfg):
    """Catatan iuran untuk gaji prorata, sesuai cara mesin: JHT/JKK/JKM/JP memakai gaji pokok + tunjangan tetap yang
    dibayar (prorata); dasar BPJS Kesehatan juga, tetapi tidak di bawah UMK bila UMK diisi (Perpres 64/2020)."""
    if cfg.get("umk"):
        return ("Iuran BPJS ikut angka prorata, tetapi dasar BPJS Kesehatan minimal UMK; cocokkan dengan tagihan BPJS "
                "(bisa menagih iuran penuh untuk bulan masuk/keluar).")
    return ("Iuran BPJS Kesehatan & Ketenagakerjaan ikut angka prorata; cocokkan dengan tagihan BPJS (bisa menagih "
            "iuran penuh untuk bulan masuk/keluar).")


def terapkan_prorata(conn, per, cara):
    """hitung --prorata kalender: isi gaji pokok/tunjangan tetap DIBAYAR untuk karyawan masuk/keluar tengah bulan yang
    belum punya nominal dari pemilik. --prorata penuh: hapus isian prorata otomatis (kembali gaji penuh).
    Nominal yang diisi pemilik sendiri (isi --gaji-pokok-dibayar) tidak pernah ditimpa."""
    diubah = []
    for k in karyawan_periode(conn, per["kode"]):
        s = saran_prorata(k, per["kode"])
        if not s:
            continue
        ket = {r["kolom"]: r["keterangan"] for r in conn.execute(
            "SELECT kolom, keterangan FROM isian WHERE periode_id=? AND karyawan_id=? AND kolom IN "
            "('gaji_pokok','tunjangan_tetap')", (per["id"], k["id"]))}
        if cara == "kalender":
            if ket:
                continue
            set_isian(conn, per, k, "gaji_pokok", teks_angka(s["gaji_pokok_prorata"]), KET_PRORATA)
            if s["tunjangan_tetap"]:
                set_isian(conn, per, k, "tunjangan_tetap", teks_angka(s["tunjangan_tetap_prorata"]), KET_PRORATA)
            diubah.append(s)
        elif cara == "penuh" and ket and all(v == KET_PRORATA for v in ket.values()):
            for kol in ket:
                set_isian(conn, per, k, kol, "-")
            diubah.append(s)
    return diubah


def info_tertunda(k, kode, e, keluar, sudah_dibayar=False, sementara_diminta=False):
    """Gagal dari riwayat_tahun -> keterangan 'tertunda' berbahasa awam (untuk pemilik) + langkah (untuk agent).
    teks = subjek + ': ' + inti [+ tanya_prorata]; inti sama untuk karyawan dengan kebutuhan sama (bisa digabung)."""
    th, bl = int(kode[:4]), int(kode[5:7])
    d = e.detail
    bm = d.get("bulan_mulai") or 1
    pertama = d.get("bulan_pertama_aplikasi") or bl
    sebab = ("keluar %s" % ftgl(date.fromisoformat(k["tanggal_keluar"]))) if keluar else "Desember"
    bisa_sementara = bool(keluar) and bl != 12 and not d.get("saldo_awal_salah")
    belum_ada = [b for b, j in d.get("bulan_kurang", []) if j == "belum ada"]
    sebelum = [b for b in belum_ada if b < pertama]          # sebelum aplikasi dipakai -> hanya lewat saldo awal
    terlewat = [b for b in belum_ada if b >= pertama]        # aplikasi sudah dipakai, bulan itu terlewat
    belum_final = [b for b, j in d.get("bulan_kurang", []) if j != "belum ada"]
    nb = lambda bs: ", ".join(nama_periode("%04d-%02d" % (th, x)) for x in bs)        # noqa: E731
    butuh, langkah = [], []
    if d.get("saldo_awal_salah"):
        butuh.append("Saldo awal yang tercatat melewati bulan ini: perbaiki angkanya.")
        langkah.append("saldo-awal --karyawan %s --tahun %d --sampai-bulan %d --bruto .. --pph21 .. --iuran .." % (
            k["kode"], th, bl - 1))
    if sebelum:
        butuh.append("Butuh total %s: (1) penghasilan bruto (angka di bukti potong bulanan, termasuk iuran JKK, "
                     "JKM & BPJS Kesehatan bagian perusahaan), (2) PPh 21 yang sudah dipotong, (3) iuran JHT 2%% + "
                     "JP 1%% yang dipotong dari gajinya." % rentang_bulan(th, bm, max(sebelum)))
        langkah.append("saldo-awal --karyawan %s --tahun %d --sampai-bulan %d --bruto <1> --pph21 <2> --iuran <3>" % (
            k["kode"], th, max(sebelum)))
    if terlewat:
        butuh.append("Gaji %s belum dihitung & dikunci di aplikasi ini: hitung dan kunci dulu bulan itu (bila gajinya "
                     "dibayar di luar aplikasi, kirim totalnya %s sebagai saldo awal)." % (
                         nb(terlewat), rentang_bulan(th, bm, max(terlewat))))
        for x in terlewat:
            langkah += ["hitung --bulan %04d-%02d" % (th, x), "final --bulan %04d-%02d (pratinjau, lalu --ya)" % (th, x)]
        if max(terlewat) < (d.get("bulan_periode_pertama") or bl):
            # bulan terlewat tepat setelah saldo awal & sebelum periode pertama: perpanjang saldo awal juga wajar
            langkah.append("atau, bila gaji %s dibayar di luar aplikasi: saldo-awal --karyawan %s --tahun %d "
                           "--sampai-bulan %d --bruto <total %s> --pph21 .. --iuran .. (menggantikan saldo awal lama)" % (
                               nb(terlewat), k["kode"], th, max(terlewat), rentang_bulan(th, bm, max(terlewat))))
    if belum_final:
        butuh.append("Gaji %s di aplikasi ini masih draf/direvisi: kunci (final) dulu bulan itu." % nb(belum_final))
        langkah += ["final --bulan %04d-%02d (pratinjau, lalu --ya)" % (th, x) for x in belum_final]
    langkah.append("hitung --bulan %s" % kode)
    inti = "%s adalah Masa Pajak Terakhir: PPh 21-nya dihitung ulang setahun. %s" % (
        nama_periode(kode), " ".join(butuh))
    if bisa_sementara:
        inti += (" Pilihan: (a) %s, lalu dihitung ulang setahun (final); atau (b) hitung bulan ini saja dengan tarif "
                 "bulanan (TER) sebagai angka SEMENTARA - wajib dilengkapi sebelum bukti potong 1721-A1 dibuat." % (
                     "kirim angka itu" if sebelum and not (terlewat or belum_final) else "lengkapi data di atas"))
    subjek = "%s (%s, %s)" % (k["nama"], k["kode"], sebab)
    pr = None if sudah_dibayar else saran_prorata(k, kode)
    tanya = ("Gaji terakhir %s penuh atau prorata %d/%d hari kalender (%s)?" % (
        k["nama"], pr["hari"], pr["hari_bulan"], pr["rumus"])) if pr else ""
    return {"kode": k["kode"], "nama": k["nama"], "alasan": "berhenti bekerja" if keluar else "Desember",
            "rentang_data": (rentang_bulan(th, bm, max(sebelum)) if sebelum else nb(terlewat or belum_final)
                             if (terlewat or belum_final) else rentang_bulan(th, bm, max(bm, bl - 1))),
            "tanggal_keluar": k["tanggal_keluar"] if keluar else "", "bulan_kurang": e.detail.get("kurang", []),
            "data_dibutuhkan": butuh, "bisa_pph_sementara": bisa_sementara,
            "sementara_diabaikan": bool(sementara_diminta and not bisa_sementara),
            "subjek": subjek, "sebab": sebab, "inti": inti, "tanya_prorata": tanya,
            "teks": "%s: %s%s" % (subjek, inti, " " + tanya if tanya else ""),
            "langkah_agent": langkah + (["atau pilihan (b): hitung --bulan %s --pph-sementara" % kode]
                                        if bisa_sementara else []),
            "saran_prorata": pr}


def baris_tertunda(tertunda):
    """Baris teks tertunda untuk pemilik: karyawan dengan kebutuhan sama digabung jadi satu baris."""
    grup, urut = {}, []
    for t in tertunda:
        kunci = t.get("inti") or t["teks"]
        if kunci not in grup:
            grup[kunci] = []
            urut.append(kunci)
        grup[kunci].append(t)
    o = []
    pagar = [t for t in tertunda if t.get("catatan_pagar")]
    for kunci in urut:
        ts = grup[kunci]
        if len(ts) == 1:
            t = ts[0]
            teks = "%s: %s" % (t["subjek"], t["inti"]) if t.get("catatan_pagar") and len(pagar) > 1 else t["teks"]
            if t.get("tambahan"):
                lain = [x["nama"] for x in tertunda if x is not t and x.get("inti") == t["tambahan"]]
                teks += (" Selain itu, data Masa Pajak Terakhir-nya juga belum ada (sama dengan %s%s)." % (
                    lain[0], " dkk." if len(lain) > 1 else "") if lain else " Selain itu: " + t["tambahan"])
            o.append(teks)
            continue
        sebab = {t.get("sebab") for t in ts}
        subjek = ("%s (%d karyawan, %s)" % (", ".join("%s (%s)" % (t["nama"], t["kode"]) for t in ts), len(ts),
                                            sebab.pop()) if len(sebab) == 1 and None not in sebab else
                  ", ".join(t.get("subjek") or t["nama"] for t in ts))
        o.append("%s: %s%s" % (subjek, kunci, "".join(" " + t["tanya_prorata"] for t in ts if t.get("tanya_prorata"))))
    if len(pagar) > 1:                       # kalimat dasar hukum persetujuan khusus cukup sekali
        o.append("Untuk %s: %s" % (", ".join(t["nama"] for t in pagar), CATATAN_PAGAR))
    abai = [t["nama"] for t in tertunda if t.get("sementara_diabaikan")]
    if abai:
        o.append("Pilihan angka sementara tidak berlaku untuk Desember (PPh 21 Desember memang dihitung ulang "
                 "setahun), jadi tidak dipakai%s." % ("" if len(abai) == len(tertunda) else
                                                      " untuk: " + ", ".join(abai)))
    return o


KOLOM_PAYROLL = ["nama", "jabatan", "ptkp", "gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap",
                 "lembur_hari_kerja", "lembur_hari_libur", "lembur_rp", "bonus", "thr", "potongan_lain", "zakat",
                 "jkk_persen", "ikut_bpjs_kesehatan", "ikut_bpjs_tk", "ikut_jp", "dtp", "bruto_tetap_januari",
                 "dasar_bpjs_kesehatan", "berhenti", "bruto_sd_bulan_lalu", "pph21_sd_bulan_lalu",
                 "iuran_sd_bulan_lalu", "zakat_sd_bulan_lalu", "bulan_mulai"]


def ada_persetujuan_khusus(conn, kode, kode_k):
    """True bila log mencatat persetujuan khusus pemilik (--ya-saya-paham) untuk dasar BPJS turun karyawan ini."""
    for (r,) in conn.execute("SELECT ringkasan FROM log WHERE perintah IN ('isi', 'isi --file')"):
        try:
            d = json.loads(r)
        except ValueError:
            continue
        kk = d.get("konfirmasi_kepatuhan") if isinstance(d, dict) else None
        if not kk or d.get("periode") != kode:
            continue
        masalah = kk.get("masalah", [])
        if (d.get("karyawan") == kode_k and "dasar_bpjs_turun_bulan_penuh" in masalah) or \
                "dasar_bpjs_turun_bulan_penuh:%s" % kode_k in masalah:
            return True
    return False


def susun_masukan(conn, per, cfg, pph_sementara=False, tunda=None, pratinjau=False):
    """Susun baris mesin per karyawan. v1.0.13: karyawan yang datanya kurang (Masa Pajak Terakhir tanpa data Januari
    s.d. bulan lalu) TIDAK menahan karyawan lain: ia masuk daftar `tertunda` (tidak dihitung), atau - bila
    pph_sementara=True dan ia keluar di bulan selain Desember - dihitung bulan ini saja dengan TER bulanan dan
    ditandai PPh 21 SEMENTARA. tunda = {karyawan_id: info} dari hitung-cepat (mis. butuh persetujuan khusus).
    Kembalikan (masukan, catatan, argv_umum, tertunda)."""
    kode = per["kode"]
    awal, akhir = rentang_periode(kode)
    daftar = karyawan_periode(conn, kode)
    if not daftar:
        raise Gagal("Tidak ada karyawan aktif di %s. Tambah karyawan dulu (gaji.py karyawan tambah)." % nama_periode(kode))
    masukan, catatan, tertunda = [], [], []
    for k in daftar:
        keluar = k["tanggal_keluar"] and awal.isoformat() <= k["tanggal_keluar"] <= akhir.isoformat()
        if tunda and k["id"] in tunda:
            info = tunda[k["id"]]
            if keluar or int(kode[5:7]) == 12:
                # tertunda karena pagar BPJS, tetapi data Masa Pajak Terakhir-nya juga kurang: sebut sekarang juga,
                # supaya pemilik tidak ditanya dua kali (persetujuan dulu, baru data Januari s.d. bulan lalu)
                try:
                    riwayat_tahun(conn, k, kode)
                except Gagal as e:
                    it = info_tertunda(k, kode, e, keluar, True)
                    info = dict(info, tambahan=it["inti"], data_dibutuhkan=info["data_dibutuhkan"] +
                                it["data_dibutuhkan"], langkah_agent=info["langkah_agent"] + [
                                    "Data Masa Pajak Terakhir juga kurang: " + " -> ".join(it["langkah_agent"])])
            tertunda.append(info)
            continue
        isi = isian_karyawan(conn, per, k)
        ket_isi = {r["kolom"]: r["keterangan"] for r in conn.execute(
            "SELECT kolom, keterangan FROM isian WHERE periode_id=? AND karyawan_id=?", (per["id"], k["id"]))}
        diisi = [c for c in ("gaji_pokok", "tunjangan_tetap") if c in isi]     # nominal DIBAYAR bulan ini
        masuk_tengah = awal.isoformat() < k["tanggal_masuk"] <= akhir.isoformat()
        row = {
            "nama": k["nama"], "jabatan": k["jabatan"], "ptkp": k["ptkp"],
            "gaji_pokok": isi.get("gaji_pokok", k["gaji_pokok"]),
            "tunjangan_tetap": isi.get("tunjangan_tetap", k["tunjangan_tetap"]),
            "tunjangan_tidak_tetap": isi.get("tunjangan_tidak_tetap", k["tunjangan_tidak_tetap"]),
            "lembur_hari_kerja": isi.get("lembur_hari_kerja", ""), "lembur_hari_libur": isi.get("lembur_hari_libur", ""),
            "lembur_rp": isi.get("lembur_rp", ""), "bonus": isi.get("bonus", ""), "thr": isi.get("thr", ""),
            "potongan_lain": teks_angka(D(isi.get("potongan_lain")) + D(isi.get("potongan_tidak_masuk"))),
            "zakat": isi.get("zakat", k["zakat"]), "jkk_persen": k["jkk_persen"],
            "ikut_bpjs_kesehatan": "ya" if k["ikut_kes"] else "tidak", "ikut_bpjs_tk": "ya" if k["ikut_tk"] else "tidak",
            "ikut_jp": "ya" if k["ikut_jp"] else "tidak", "dtp": "ya" if k["dtp"] else "tidak",
            "bruto_tetap_januari": k["bruto_tetap_januari"], "dasar_bpjs_kesehatan": k["dasar_bpjs_kesehatan"],
            "berhenti": "ya" if keluar else "tidak",
        }
        mt, sementara = None, None
        if keluar or int(kode[5:7]) == 12:
            try:
                bm, tot, sumber = riwayat_tahun(conn, k, kode)
            except Gagal as e:
                info = info_tertunda(k, kode, e, keluar, bool(diisi), pph_sementara)
                if not (pph_sementara and info["bisa_pph_sementara"]):
                    tertunda.append(info)
                    continue
                # pilihan (b): bulan ini saja, TER bulanan (mesin: berhenti=tidak); ditandai SEMENTARA
                row["berhenti"] = "tidak"
                sementara = info
            else:
                row.update({"bruto_sd_bulan_lalu": teks_angka(tot["bruto"]),
                            "pph21_sd_bulan_lalu": teks_angka(tot["pph"]),
                            "iuran_sd_bulan_lalu": teks_angka(tot["iuran"]),
                            "zakat_sd_bulan_lalu": teks_angka(tot["zakat"]), "bulan_mulai": str(bm)})
                mt = {"alasan": "berhenti bekerja" if keluar else "Desember", "bulan_mulai": bm,
                      "bruto_sd_bulan_lalu": tot["bruto"], "pph21_sd_bulan_lalu": tot["pph"],
                      "iuran_sd_bulan_lalu": tot["iuran"], "zakat_sd_bulan_lalu": tot["zakat"], "sumber": sumber}
        for ps in masalah_kepatuhan(dict(k), cfg).values():
            catatan.append(ps + " Wajib menurut " + DASAR_KEPATUHAN.split(";")[0] + ". Bila iuran sudah dibayar "
                           "lewat sistem lain, pastikan tercatat; bila belum, daftarkan/perbaiki data BPJS karyawan ini.")
        for ps in masalah_dasar_turun(k, isi, kode).values():
            if pratinjau:          # hitung-cepat dengan persetujuan khusus; pratinjau berisi alasan (str) atau True
                ket = "(Dipakai atas persetujuan khusus pemilik; belum disimpan, dicatat saat disimpan.%s)" % (
                    " Alasan: %s." % pratinjau.rstrip(".") if isinstance(pratinjau, str) and pratinjau else "")
            elif ada_persetujuan_khusus(conn, kode, k["kode"]):
                ket = "(Disimpan dengan persetujuan khusus pemilik, tercatat di log.)"
            else:
                ket = "(Tidak ada catatan persetujuan khusus pemilik untuk isian ini; pastikan ada alasan sah.)"
            # teks pemilik: nama bulan & "(bukan bulan masuk/keluar)" sudah jelas dari rekap bulan ini
            catatan.append(ps.split(" Bila gaji memang dipotong")[0].replace(" (bukan bulan masuk/keluar)", "").replace(
                " " + nama_periode(kode) + " diisi", " diisi") + " " + ket)
        pr = saran_prorata(k, kode)
        if pr and not diisi:
            sebab = ("masuk %s" % ftgl(date.fromisoformat(k["tanggal_masuk"]))) if masuk_tengah else (
                "keluar %s" % ftgl(date.fromisoformat(k["tanggal_keluar"])))
            catatan.append("%s %s (tengah bulan): gaji dihitung PENUH (asumsi; ikut perjanjian kerja). Bila prorata hari "
                           "kalender (%d dari %d hari): %s. Mohon pastikan mana yang dipakai." % (
                               k["nama"], sebab, pr["hari"], pr["hari_bulan"], pr["rumus"]))
        elif pr and ket_isi.get("gaji_pokok") == KET_PRORATA:
            catatan.append("%s: gaji diprorata hari kalender (asumsi, %d dari %d hari): %s. %s" % (
                k["nama"], pr["hari"], pr["hari_bulan"], pr["rumus"], catatan_iuran_prorata(cfg)))
        elif pr and len(diisi) == 1:
            # hanya satu komponen yang diisi nominal dibayarnya: komponen lain tetap penuh -> sebut dalam satu kalimat
            lain = "tunjangan_tetap" if diisi[0] == "gaji_pokok" else "gaji_pokok"
            if D(k[lain]):
                label = {"gaji_pokok": "gaji pokok", "tunjangan_tetap": "tunjangan tetap"}
                catatan.append("%s: %s bulan ini diisi %s; %s %s tetap dihitung penuh. Bila juga dibayar sebagian, "
                               "sebutkan nominalnya." % (k["nama"], label[diisi[0]], rp(D(isi[diisi[0]])),
                                                         label[lain], rp(D(k[lain]))))
        masukan.append({"k": k, "row": row, "isi": isi, "masa_terakhir": mt, "keluar": bool(keluar),
                        "masuk_tengah": masuk_tengah, "sementara": sementara})
    if not masukan:
        raise Gagal("Belum ada karyawan yang bisa dihitung untuk %s. Data yang kurang:\n- %s" % (
            nama_periode(kode), "\n- ".join(baris_tertunda(tertunda))), tertunda=tertunda)
    argv_umum = ["--periode", kode, "--format", "json", "--perusahaan", re.sub(r"[;,]", " ", cfg["nama_usaha"] or "")]
    if cfg["umk"]:
        argv_umum += ["--umk", cfg["umk"]]
    if cfg["jkk"]:
        argv_umum += ["--jkk", cfg["jkk"]]
    if cfg["batas_jp"]:
        argv_umum += ["--batas-jp", cfg["batas_jp"]]
    return masukan, catatan, argv_umum, tertunda


def hitung_periode(conn, per, cfg, tmp, pph_sementara=False, tunda=None, pratinjau=False):
    """Jalankan mesin payroll (per kelompok pola hari kerja). Kembalikan (hasil per karyawan, total, peringatan, sidik).
    Karyawan tertunda (data kurang) tidak dihitung; daftarnya ada di total["tertunda"]."""
    masukan, catatan, argv_umum, tertunda = susun_masukan(conn, per, cfg, pph_sementara, tunda, pratinjau)
    kelompok = {}
    for m in masukan:
        kelompok.setdefault(m["k"]["hari_kerja"], []).append(m)
    sidik = hashlib.sha256()
    hasil, peringatan, dihitung = [], list(catatan), []
    for hk in sorted(kelompok):
        grup = kelompok[hk]
        f = os.path.join(tmp, "masukan-%d.csv" % hk)
        argv = ["--data", f, "--hari-kerja", str(hk), "--out", os.path.join(tmp, "out-%d" % hk)] + argv_umum
        isi_csv = tulis_csv_mesin(f, KOLOM_PAYROLL, [m["row"] for m in grup])
        try:
            out = jalankan_mesin("payroll.py", argv)
        except Gagal as e:
            if e.detail.get("mesin") != "payroll.py" or BARIS_DITOLAK not in e.pesan:
                raise                       # galat umum (mis. batas upah JP periode belum tercatat): tetap satu pesan
            # v1.0.13: satu baris yang ditolak mesin tidak menahan karyawan lain -> cari barisnya, tandai tertunda
            salah = baris_ditolak_mesin(grup, hk, argv_umum, tmp)
            if not salah:
                raise
            tertunda += [t for _, t in salah]
            buang = [id(m) for m, _ in salah]
            grup = [m for m in grup if id(m) not in buang]
            if not grup:
                continue
            isi_csv = tulis_csv_mesin(f, KOLOM_PAYROLL, [m["row"] for m in grup])
            out = jalankan_mesin("payroll.py", argv)
        sidik.update(isi_csv.encode("utf-8"))
        sidik.update(json.dumps(argv_umum + [str(hk)]).encode("utf-8"))
        if len(out["karyawan"]) != len(grup):
            raise Gagal("Jumlah hasil mesin tidak cocok dengan jumlah karyawan.")
        for m, p in zip(grup, out["karyawan"]):
            if bersih(re.sub(r"[;,\t\"]", " ", m["row"]["nama"])) != bersih(p["nama"]):
                raise Gagal("Urutan hasil mesin tidak cocok (%s vs %s)." % (m["row"]["nama"], p["nama"]))
            p["peringatan"] = [x.replace(p["nama"] + ":", m["k"]["nama"] + ":", 1) for x in p["peringatan"]]
            if "gaji_pokok" in m["isi"] or "tunjangan_tetap" in m["isi"]:
                p["peringatan"] = [x + catatan_umk_dibayar(m["k"], cfg) if "di bawah UMK" in x else x
                                   for x in p["peringatan"]]
            dihitung.append(m)
            hasil.append({"kode": m["k"]["kode"], "karyawan_id": m["k"]["id"], "nama": m["k"]["nama"],
                          "jabatan": m["k"]["jabatan"], "ptkp": m["k"]["ptkp"], "hari_kerja": hk,
                          "tanggal_masuk": m["k"]["tanggal_masuk"], "tanggal_keluar": m["k"]["tanggal_keluar"],
                          "berhenti": m["keluar"], "masuk_tengah_bulan": m["masuk_tengah"], "isian": m["isi"],
                          "potongan_tidak_masuk": D(m["isi"].get("potongan_tidak_masuk")),
                          "potongan_lain_saja": D(m["isi"].get("potongan_lain")),
                          "masa_terakhir": m["masa_terakhir"], "payroll": p,
                          "pph_sementara": bool(m["sementara"]), "masa_terakhir_tertunda": m["sementara"]})
            peringatan += p["peringatan"]
        for x in out.get("peringatan_umum", []):
            if x not in peringatan:
                peringatan.append(x)
    if not hasil:
        raise Gagal("Belum ada karyawan yang bisa dihitung untuk %s. Data yang kurang:\n- %s" % (
            nama_periode(per["kode"]), "\n- ".join(baris_tertunda(tertunda))), tertunda=tertunda)
    hasil.sort(key=lambda h: h["kode"])
    tertunda.sort(key=lambda t: t["kode"])
    total = total_perusahaan(hasil)
    total["tertunda"] = tertunda
    return hasil, total, peringatan_jkk(peringatan, dihitung, cfg), sidik.hexdigest()


def catatan_umk_dibayar(k, cfg):
    """Tambahan untuk peringatan UMK mesin bila bulan ini diisi gaji yang DIBAYAR (prorata/sebagian): UMK berlaku untuk
    gaji penuh sebulan, jadi bandingkan dengan gaji penuh di data karyawan (dihitung di sini, bukan oleh pemilik)."""
    penuh = D(k["gaji_pokok"]) + D(k["tunjangan_tetap"])
    if cfg.get("umk") and penuh >= D(cfg["umk"]):
        return (" (Bulan ini diisi gaji yang DIBAYAR/prorata; gaji penuh sebulan di data karyawan %s tidak di bawah "
                "UMK - UMK berlaku untuk gaji penuh sebulan.)" % rp(penuh))
    return " (Bulan ini diisi gaji yang DIBAYAR/prorata; gaji penuh sebulan di data karyawan %s juga di bawah UMK.)" % (
        rp(penuh))


JKK_BELUM = "Tarif JKK belum diisi"      # awal peringatan umum mesin bila tarif JKK umum (--jkk) tidak diberikan


def peringatan_jkk(peringatan, dihitung, cfg):
    """Mesin selalu memberi 'Tarif JKK belum diisi: dipakai 0,24%' bila tarif JKK umum kosong, walaupun tiap karyawan
    punya tarif sendiri di data (yang benar-benar dipakai mesin). Ganti dengan kalimat yang sesuai; mesin tidak diubah."""
    if cfg.get("jkk") or not any(x.startswith(JKK_BELUM) for x in peringatan):
        return peringatan
    tk = [m for m in dihitung if m["k"]["ikut_tk"]]
    kosong = [m["k"]["nama"] for m in tk if not str(m["row"]["jkk_persen"] or "").strip()]
    if tk and len(kosong) == len(tk):
        return peringatan                                   # benar: semua memakai 0,24%
    per_tarif = {}
    for m in tk:
        if str(m["row"]["jkk_persen"] or "").strip():
            per_tarif.setdefault(tc.format_persen(D(m["row"]["jkk_persen"])), []).append(m["k"]["nama"])
    ganti = []
    if per_tarif:
        siapa = lambda ns: ", ".join(ns) if len(ns) <= 3 else "%d karyawan" % len(ns)      # noqa: E731
        kal = "Tarif JKK dari data karyawan: %s" % (
            next(iter(per_tarif)) if len(per_tarif) == 1 and not kosong else
            ", ".join("%s (%s)" % (t, siapa(ns)) for t, ns in per_tarif.items()))
        if kosong:
            kal += ("; belum diisi untuk %s: dipakai 0,24%% (risiko sangat rendah) - ganti dengan tarif di penetapan "
                    "BPJS Ketenagakerjaan" % siapa(kosong))
        ganti = [kal + "."]
    o = []
    for x in peringatan:
        if x.startswith(JKK_BELUM):
            o += ganti
            ganti = []
        else:
            o.append(x)
    return o


BARIS_DITOLAK = "data berikut harus diperbaiki"     # teks mesin slip-gaji-bpjs untuk galat per baris


def baris_ditolak_mesin(grup, hk, argv_umum, tmp):
    """Jalankan mesin per karyawan untuk menemukan baris yang ditolak. Kembalikan [(masukan, info_tertunda)]."""
    salah = []
    for i, m in enumerate(grup):
        f1 = os.path.join(tmp, "cek-%d-%d.csv" % (hk, i))
        tulis_csv_mesin(f1, KOLOM_PAYROLL, [m["row"]])
        try:
            jalankan_mesin("payroll.py", ["--data", f1, "--hari-kerja", str(hk), "--out",
                                          os.path.join(tmp, "cek-out")] + argv_umum)
        except Gagal as e:
            if e.detail.get("mesin") != "payroll.py" or BARIS_DITOLAK not in e.pesan:
                raise
            alasan = "; ".join(b[2:].strip() for b in e.pesan.splitlines() if b.startswith("- ")) or \
                e.pesan.splitlines()[-1]
            k = m["k"]
            for awalan in (k["nama"] + ":", bersih(re.sub(r"[;,\t\"]", " ", k["nama"])) + ":"):
                if alasan.startswith(awalan):
                    alasan = alasan[len(awalan):].strip()
                    break
            salah.append((m, {"kode": k["kode"], "nama": k["nama"], "alasan": "data perlu diperbaiki",
                              "tanggal_keluar": "", "bulan_kurang": [], "data_dibutuhkan": [alasan],
                              "bisa_pph_sementara": False, "rentang_data": "",
                              "teks": "%s (%s): data perlu diperbaiki dulu sebelum dihitung: %s" % (
                                  k["nama"], k["kode"], alasan),
                              "langkah_agent": ["perbaiki komponen/data karyawan %s (isi / karyawan ubah)" % k["kode"],
                                                "hitung --bulan %s" % argv_umum[1]],
                              "saran_prorata": None}))
    return salah


def total_perusahaan(hasil):
    t = {k: NOL for k in ("gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap", "lembur", "bonus_thr",
                          "total_pendapatan", "bruto_pajak", "potongan_karyawan", "take_home_pay", "biaya_perusahaan",
                          "bpjs_kes_perusahaan", "bpjs_kes_karyawan", "jht_perusahaan", "jht_karyawan", "jkk", "jkm",
                          "jp_perusahaan", "jp_karyawan", "setor_bpjs_kesehatan", "setor_bpjs_ketenagakerjaan",
                          "pph21_terutang", "pph21_dipotong", "pph21_dtp", "setor_pph21", "pph21_dtp_tunai",
                          "pengembalian_pph21",
                          "potongan_tidak_masuk", "potongan_lain", "zakat")}
    for h in hasil:
        p = h["payroll"]
        pd, pt, i = p["pendapatan"], p["potongan"], p["iuran"]
        t["gaji_pokok"] += D(pd["Gaji pokok"])
        t["tunjangan_tetap"] += D(pd["Tunjangan tetap"])
        t["tunjangan_tidak_tetap"] += D(pd["Tunjangan tidak tetap"])
        t["lembur"] += D(pd["Lembur"])
        t["bonus_thr"] += D(pd["Bonus/THR"])
        t["total_pendapatan"] += D(p["total_pendapatan"])
        t["bruto_pajak"] += D(p["pph_info"]["bruto"])
        t["potongan_karyawan"] += D(p["total_potongan"])
        t["take_home_pay"] += D(p["take_home_pay"])
        t["biaya_perusahaan"] += D(p["biaya_perusahaan"])
        t["bpjs_kes_perusahaan"] += D(i["kes_perusahaan"])
        t["bpjs_kes_karyawan"] += D(i["kes_karyawan"])
        for c in ("jht_perusahaan", "jht_karyawan", "jkk", "jkm", "jp_perusahaan", "jp_karyawan"):
            t[c] += D(i[c])
        t["pph21_terutang"] += D(p["pph"])
        t["pph21_dipotong"] += D(pt["PPh 21"])
        t["pph21_dtp_tunai"] += D(pd["PPh 21 DTP dibayar tunai"])
        t["pengembalian_pph21"] += D(pd["Pengembalian kelebihan PPh 21"])
        t["potongan_tidak_masuk"] += D(h["potongan_tidak_masuk"])
        t["potongan_lain"] += D(h["potongan_lain_saja"])
        t["zakat"] += D(pt["Zakat"])
    t["setor_bpjs_kesehatan"] = t["bpjs_kes_perusahaan"] + t["bpjs_kes_karyawan"]
    t["setor_bpjs_ketenagakerjaan"] = sum((t[c] for c in ("jht_perusahaan", "jht_karyawan", "jkk", "jkm",
                                                           "jp_perusahaan", "jp_karyawan")), NOL)
    t["pph21_dtp"] = t["pph21_dtp_tunai"]
    t["jumlah_karyawan"] = len(hasil)
    return lengkapi_total(t)


def lengkapi_total(t):
    """PPh 21 per masa di SPT Masa dihitung agregat seluruh karyawan: kelebihan potong Masa Pajak Terakhir yang
    dikembalikan ke karyawan mengurangi PPh 21 yang disetor masa itu; bila hasilnya minus = lebih bayar yang dapat
    diperhitungkan ke masa berikutnya (PMK 168/2023 Pasal 21 ayat (1) & (3); artikel DJP 12-03-2025).
    - pph21_dipotong  : jumlah PPh 21 positif yang DIPOTONG dari gaji bulan ini, TERMASUK bagian DTP
                        (PMK 105/2025: PPh 21 DTP tetap dipotong lalu dibayar tunai ke karyawan)
    - pph21_dtp       : bagian PPh 21 DTP (= pph21_dtp_tunai); dibayar tunai ke karyawan, TIDAK disetor
    - pengembalian_pph21: kelebihan potong yang dikembalikan ke karyawan (sudah di gaji bersih)
    - pph21_disetor_ke_negara: PERKIRAAN setor = max(0, dipotong - DTP - dikembalikan)
    - setor_pph21     : sama dengan pph21_disetor_ke_negara (nama lama, dipertahankan untuk kompatibilitas)
    - lebih_bayar_pph21: max(0, dikembalikan - (dipotong - DTP))
    Total tersimpan versi lama (<= 1.0.10) belum punya pph21_dtp; di sana pph21_dipotong berisi jumlah yang disetor
    (tanpa DTP) dan pada v1.0.0 kunci itu belum ada (setor_pph21 = jumlah tersebut). Dilengkapi otomatis di sini."""
    t = dict(t)
    dtp = D(t.get("pph21_dtp_tunai"))
    if "pph21_dtp" not in t:                       # total lama: ubah ke arti baru
        lama = t["pph21_dipotong"] if "pph21_dipotong" in t else t.get("setor_pph21", NOL)
        t["pph21_dipotong"] = D(lama) + dtp
        t["pph21_dtp"] = dtp
    dipotong, dtp, kembali = D(t["pph21_dipotong"]), D(t["pph21_dtp"]), D(t.get("pengembalian_pph21"))
    wajib_setor = max(dipotong - dtp, NOL)
    t["pph21_disetor_ke_negara"] = max(wajib_setor - kembali, NOL)
    t["setor_pph21"] = t["pph21_disetor_ke_negara"]
    t["lebih_bayar_pph21"] = max(kembali - wajib_setor, NOL)
    return t


def baris_setor_pph21(total, hasil=None):
    dipotong, kembali = D(total["pph21_dipotong"]), D(total.get("pengembalian_pph21"))
    dtp = D(total.get("pph21_dtp"))
    if not kembali and not dtp:
        return ["- Setor PPh 21: %s" % rp(total["setor_pph21"])]
    if not kembali:
        return ["- PPh 21 dipotong dari gaji bulan ini: %s (termasuk DTP %s yang dibayar tunai ke karyawan dan tidak "
                "disetor, PMK 105/2025)" % (rp(dipotong), rp(dtp)),
                "- Setor PPh 21 ke negara: %s" % rp(total["setor_pph21"])]
    o = ["- PPh 21 dipotong bulan ini: %s" % rp(dipotong)]
    if dtp:
        o.append("- Bagian PPh 21 DTP (dibayar tunai ke karyawan, tidak disetor, PMK 105/2025): %s" % rp(dtp))
    siapa = [h["nama"] for h in hasil or [] if D(h["payroll"]["pendapatan"].get("Pengembalian kelebihan PPh 21"))]
    siapa = (", ".join(siapa) if len(siapa) <= 3 else "%d karyawan" % len(siapa)) + ", " if siapa else ""
    o += [
         "- Kelebihan PPh 21 dikembalikan ke karyawan (%ssudah di gaji bersih): %s" % (
             siapa, rp(kembali)),
         "- Perkiraan setor PPh 21: %s (dipotong%s - dikembalikan; SPT Masa digabung semua karyawan, PMK 168/2023 "
         "Pasal 21)" % (rp(total["setor_pph21"]), " - DTP" if dtp else "")]
    if D(total.get("lebih_bayar_pph21")):
        o.append("- Lebih bayar PPh 21 %s: tidak disetor; bisa diperhitungkan ke PPh 21 bulan berikutnya lewat SPT Masa "
                 "(Pasal 21 ayat (3)), tidak otomatis." % rp(total["lebih_bayar_pph21"]))
    o.append("  Kelebihan dikembalikan ke karyawan paling lambat akhir bulan berikutnya%s. Konfirmasi angka setor ke "
             "konsultan pajak/Coretax sebelum membayar." % ("; DTP tidak dikembalikan" if dtp else ""))
    return o


def ke_json(o):
    if isinstance(o, Decimal):
        return tc.angka_json(o)
    if isinstance(o, dict):
        return {k: ke_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [ke_json(v) for v in o]
    if isinstance(o, sqlite3.Row):
        return {k: o[k] for k in o.keys()}
    return o


# --------------------------------------------------------------------------- teks pemilik: peringatan ringkas & awam
_ISTILAH = [("isi tarif JKK (kolom jkk_persen / --jkk) dengan angka itu", "pakai tarif itu"),
            ("kolom iuran_sd_bulan_lalu (JHT+JP karyawan Jan s.d. bulan lalu) kosong",
             "iuran JHT+JP karyawan Januari s.d. bulan lalu belum diisi"),
            ("kolom bruto_tetap_januari kosong", "bruto tetap Januari belum diisi"),
            ("take home pay negatif", "gaji bersih minus")]
_POLA_BPJS = re.compile(r"^TIDAK didaftarkan BPJS (Kesehatan|Ketenagakerjaan)")
_POLA_UMK = re.compile(r"^gaji pokok \+ tunjangan tetap (Rp [\d.]+) di bawah UMK yang Anda isi \((Rp [\d.]+)\)\.(.*)$")
_POLA_UMK_PENUH = re.compile(r"gaji penuh sebulan di data karyawan (Rp [\d.]+) (tidak|juga) di bawah UMK")
_POLA_PENUH = re.compile(r"^((?:masuk|keluar) [\d/]+) \(tengah bulan\): gaji dihitung PENUH .*?\((\d+ dari \d+ hari)\): "
                         r"(.+?)\. Mohon pastikan")
_POLA_PRORATA = re.compile(r"^gaji diprorata hari kalender \(asumsi, (\d+ dari \d+ hari)\): (.+?)\. (Iuran .*)$")
_POLA_JKK_NETO = re.compile(r"^tarif JKK (\S+) adalah porsi JKK setelah 0,14% dialihkan untuk JKP .*? Iuran JKK yang "
                            r"dibayar tetap (\S+) \(PP 44/2015 Pasal 16\)")
# sudah tampil di "Yang harus dibayar/disetor" (baris kelebihan PPh 21 dikembalikan) -> tidak diulang di teks pemilik
_POLA_LEBIH_POTONG = re.compile(r"^PPh 21 lebih potong Rp [\d.]+ dikembalikan ke karyawan di slip ini\.$")


def awam(teks):
    """Terjemahkan nama kolom/opsi teknis dari mesin ke bahasa sehari-hari."""
    for a, b in _ISTILAH:
        teks = teks.replace(a, b)
    teks = re.sub(r"\s*\(?--[a-z][a-z-]*\)?", "", teks)
    return re.sub(r"\b[a-z]+(?:_[a-z0-9]+)+\b", lambda m: m.group(0).replace("_", " "), teks)


def ringkas_peringatan(peringatan, nama_karyawan, jumlah, asumsi=None):
    """Peringatan untuk teks pemilik: istilah teknis diterjemahkan, peringatan yang sama untuk banyak karyawan
    digabung jadi satu kalimat, dan yang sudah ada di 'Asumsi' tidak diulang. JSON tetap memakai daftar rinci."""
    asumsi = " ".join(asumsi or [])
    urut = sorted(set(nama_karyawan), key=len, reverse=True)
    blok, isi = [], {}

    def taruh(kunci, nilai):
        if kunci not in isi:
            isi[kunci] = []
            blok.append(kunci)
        isi[kunci].append(nilai)

    for x in peringatan:
        if (x.startswith((JKK_BELUM, "Tarif JKK dari data")) and "Tarif JKK" in asumsi) or \
                (x.startswith("UMK tidak diisi") and "UMK" in asumsi):
            continue
        nama, sisa = None, x
        for n in urut:
            if x.startswith(n + ": ") or x.startswith(n + " "):
                nama, sisa = n, x[len(n):].lstrip(": ").lstrip()
                break
        sisa = awam(sisa.split(" Wajib menurut UU 24/2011")[0])
        if nama is None:
            taruh(("umum", sisa), None)
            continue
        m = _POLA_BPJS.match(sisa)
        if m:
            taruh(("bpjs",), (nama, m.group(1)))
            continue
        if _POLA_LEBIH_POTONG.match(sisa):
            continue
        m = _POLA_UMK.match(sisa)
        if m:
            mp = _POLA_UMK_PENUH.search(m.group(3))
            if mp and mp.group(2) == "tidak":
                continue                    # dibayar sebagian, tetapi gaji penuh sebulannya tidak di bawah UMK
            taruh(("umk", m.group(2)), (nama, mp.group(1) if mp else m.group(1)))
            continue
        m = _POLA_PENUH.match(sisa)
        if m:
            taruh(("penuh",), (nama, m.group(1), m.group(2), m.group(3)))
            continue
        m = _POLA_PRORATA.match(sisa)
        if m:
            taruh(("prorata", m.group(3)), (nama, m.group(2)))
            continue
        m = _POLA_JKK_NETO.match(sisa)
        if m:
            sisa = ("tarif JKK %s adalah porsi JKK murni (0,14%% sudah dialihkan ke JKP, PP 6/2025); iuran JKK yang "
                    "dibayar perusahaan %s (PP 44/2015 Pasal 16) - pakai %s kecuali tagihan BPJS menyebut lain." % (
                        m.group(1), m.group(2), m.group(2)))
        taruh(("sama", sisa), nama)
    o = []
    for kunci in blok:
        v = isi[kunci]
        if kunci[0] == "umum":
            o.append(kunci[1])
        elif kunci[0] == "bpjs":
            per = {}
            for n, j in v:
                per.setdefault(n, []).append(j)
            o.append("Tidak didaftarkan BPJS: %s. Pekerja penerima upah wajib didaftarkan dengan upah sebenarnya (UU "
                     "24/2011 Pasal 15); bila iurannya dibayar lewat sistem lain, pastikan tercatat." % "; ".join(
                         "%s (%s)" % (n, " & ".join(js)) for n, js in per.items()))
        elif kunci[0] == "umk":
            per_upah = {}                                   # gaji sama -> satu kelompok (hemat panjang teks)
            for n, u in v:
                per_upah.setdefault(u, []).append(n)
            o.append("Gaji pokok + tunjangan tetap sebulan penuh di bawah UMK yang Anda isi (%s): %s. Pastikan tidak "
                     "melanggar upah minimum (usaha mikro/kecil punya aturan tersendiri)." % (kunci[1], "; ".join(
                         "%s (%s%s)" % (", ".join(ns), "masing-masing " if len(ns) > 1 else "", u)
                         for u, ns in per_upah.items())))
        elif kunci[0] == "penuh":
            o.append("Masuk/keluar tengah bulan, gaji dihitung PENUH (asumsi; ikut perjanjian kerja). Bila prorata hari "
                     "kalender: %s. Mohon pastikan mana yang dipakai." % "; ".join(
                         "%s (%s): %s" % (n, sb, r) for n, sb, h, r in v))
        elif kunci[0] == "prorata":
            o.append("Gaji diprorata hari kalender (asumsi): %s. %s" % (
                "; ".join("%s, %s" % (n, r) for n, r in v), kunci[1]))
        else:
            nama = list(dict.fromkeys(v))
            if len(nama) == 1:
                o.append("%s: %s" % (nama[0], kunci[1]))
            elif len(nama) == jumlah:
                o.append("Semua karyawan (%d): %s" % (jumlah, kunci[1]))
            else:
                o.append("%s (%d karyawan): %s" % (", ".join(nama), len(nama), kunci[1]))
    return o


STATUS_TEKS = {"draf": "DRAF (belum final)", "final": "FINAL (terkunci)",
               "pratinjau": "PRATINJAU (hitung cepat, belum disimpan)"}


def teks_rekap(kode, per_status, revisi, hasil, total, peringatan, cfg, asumsi=None):
    """Teks rekap untuk pemilik (bahasa awam, tanpa nama perintah/jalur file)."""
    judul = "REKAP GAJI %s - %s" % (nama_periode(kode).upper(), cfg["nama_usaha"] or "(nama usaha)")
    tertunda = total.get("tertunda") or []
    sementara = [h for h in hasil if h.get("pph_sementara")]
    jumlah = "%d karyawan%s" % (len(hasil), " dihitung, %d tertunda" % len(tertunda) if tertunda else "")
    o = [judul, "Status: %s%s | %s" % (STATUS_TEKS[per_status], " | revisi ke-%d" % revisi if revisi else "", jumlah),
         "", "| Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |",
         "|---|---|---:|---:|---:|---:|---:|"]
    rpt = lambda x: rp(x).replace("Rp ", "")                                   # noqa: E731  (tabel: dalam rupiah)
    for h in hasil:
        p = h["payroll"]
        tanda = ""
        if h["berhenti"]:
            tanda = " (keluar)"
        elif h["masuk_tengah_bulan"]:
            tanda = " (baru)"
        pph = rpt(p["pph"]) + (" DTP" if p["dtp"] else "") + (" *" if h["masa_terakhir"] else "") + (
            " (sementara)" if h.get("pph_sementara") else "")
        o.append("| %s | %s%s | %s | %s | %s | %s | %s |" % (
            h["kode"], h["nama"], tanda, rpt(p["total_pendapatan"]), rpt(p["total_potongan"]), pph,
            rpt(p["take_home_pay"]), rpt(p["biaya_perusahaan"])))
    o.append("| | **Total** | **%s** | **%s** | **%s** | **%s** | **%s** |" % (
        rpt(total["total_pendapatan"]), rpt(total["potongan_karyawan"]), rpt(total["pph21_terutang"]),
        rpt(total["take_home_pay"]), rpt(total["biaya_perusahaan"])))
    o.append("(angka tabel dalam rupiah)")
    if any(h["masa_terakhir"] for h in hasil):
        o.append("* PPh 21 dihitung ulang setahun (Masa Pajak Terakhir: Desember/bulan keluar).")
    for h in sementara:
        info = h.get("masa_terakhir_tertunda") or {}
        o.append("(sementara) PPh 21 %s dihitung untuk bulan ini saja dengan tarif efektif bulanan (TER) karena data "
                 "%s belum ada. Perhitungan setahun (Masa Pajak Terakhir) BELUM FINAL - wajib dilengkapi sebelum "
                 "bukti potong 1721-A1 (BPA1) dibuat; PPh 21 dan gaji bersihnya bisa berubah." % (
                     h["nama"], info.get("rentang_data", "Januari s.d. bulan lalu")))
    kepala = "Yang harus dibayar/disetor:"
    if tertunda:
        kepala = "Yang harus dibayar/disetor (BELUM termasuk yang tertunda: %s):" % ", ".join(
            t["nama"] for t in tertunda)
    o += ["", kepala,
          "- Transfer gaji bersih ke karyawan: %s" % rp(total["take_home_pay"]),
          "- Setor BPJS Kesehatan (4%% perusahaan + 1%% karyawan): %s" % rp(total["setor_bpjs_kesehatan"]),
          "- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): %s" % rp(total["setor_bpjs_ketenagakerjaan"])]
    o += baris_setor_pph21(total, hasil)
    if sementara:
        o.append("  Setoran PPh 21 ini memakai angka SEMENTARA untuk %s; angka finalnya bisa berubah setelah data "
                 "lengkap." % ", ".join("%s (%s)" % (h["nama"], rp(h["payroll"]["pph"])) for h in sementara))
    if total["pph21_dtp_tunai"]:
        o.append("- PPh 21 DTP dibayar tunai ke karyawan (sudah di gaji bersih): %s" % rp(total["pph21_dtp_tunai"]))
    o.append("- Total biaya gaji perusahaan: %s" % rp(total["biaya_perusahaan"]))
    if tertunda:
        o += ["", "TERTUNDA - belum dihitung, menunggu data:"] + ["- " + x for x in baris_tertunda(tertunda)]
    if asumsi:
        o += ["", "Asumsi yang perlu Anda cek:"] + ["%d. %s" % (i, x) for i, x in enumerate(asumsi, 1)]
    ringkas = ringkas_peringatan(peringatan, [h["nama"] for h in hasil] + [t["nama"] for t in tertunda], len(hasil),
                                 asumsi)
    if ringkas:
        o += ["", "Perlu diperhatikan:"] + ["- " + x for x in ringkas]
    o += ["", "_" + DISCLAIMER + "_"]
    return "\n".join(o)


def penutup_pembeli(total, hasil):
    """Kalimat penutup rekap draf untuk pemilik (tanpa perintah)."""
    tunda = [t["nama"] for t in (total.get("tertunda") or [])] + [h["nama"] for h in hasil if h.get("pph_sementara")]
    if tunda:
        return ("Periode ini belum bisa dikunci (final) sampai data %s lengkap. Angka karyawan lain di atas sudah bisa "
                "diperiksa sekarang." % ", ".join(tunda))
    return "Sudah benar? Kalau ya, balas \"kunci\" - setelah dikunci, slip dan file transfer dibuat."


def langkah_agent(kode, total, hasil, peringatan, saran, prorata_diterapkan):
    """Langkah lanjutan untuk AGENT (berisi nama perintah - jangan ditempel ke chat pemilik)."""
    o = []
    for t in total.get("tertunda") or []:
        o.append("Tertunda %s: %s" % (t["nama"], " -> ".join(t["langkah_agent"])))
    for h in hasil:
        if h.get("pph_sementara"):
            o.append("PPh 21 sementara %s: setelah pemilik memberi data, saldo-awal ... lalu hitung --bulan %s (tanpa "
                     "--pph-sementara)" % (h["nama"], kode))
    if saran:
        o.append("Masuk/keluar tengah bulan dihitung penuh (%s). Bila pemilik memilih prorata hari kalender: hitung "
                 "--bulan %s --prorata kalender; nominal lain: isi --bulan %s --karyawan <kode> --gaji-pokok-dibayar .. "
                 "[--tunjangan-tetap-dibayar ..]" % (", ".join(x["nama"] for x in saran), kode, kode))
    if prorata_diterapkan:
        o.append("Prorata hari kalender diterapkan (%s). Bila pemilik memilih gaji penuh: hitung --bulan %s --prorata "
                 "penuh" % (", ".join(x["nama"] for x in prorata_diterapkan), kode))
    if any("TIDAK didaftarkan BPJS" in x or "dasar iuran BPJS Kesehatan diisi" in x for x in peringatan):
        o.append("Data BPJS yang diperingatkan: karyawan ubah --karyawan <kode> --bpjs kes,tk,jp / "
                 "--dasar-bpjs-kesehatan - (pratinjau, lalu --ya setelah pemilik setuju)")
    o.append("Slip draf per karyawan: slip --bulan %s" % kode)
    if not (total.get("tertunda") or any(h.get("pph_sementara") for h in hasil)):
        o.append("Kunci setelah pemilik setuju: final --bulan %s (pratinjau, lalu --ya)" % kode)
    return o


def muat_hasil(conn, per, revisi=None):
    rev = per["revisi"] if revisi is None else revisi
    hp = conn.execute("SELECT * FROM hasil_periode WHERE periode_id=? AND revisi=?", (per["id"], rev)).fetchone()
    if not hp:
        return None
    rows = conn.execute("SELECT data FROM hasil WHERE periode_id=? AND revisi=? ORDER BY karyawan_id",
                        (per["id"], rev)).fetchall()
    hasil = sorted((json.loads(r["data"]) for r in rows), key=lambda h: h["kode"])
    return {"hasil": hasil, "total": ke_json(lengkapi_total(json.loads(hp["total"]))),
            "peringatan": json.loads(hp["peringatan"]),
            "dihitung": hp["dihitung"], "sidik": hp["sidik"], "revisi": rev}


def cmd_hitung(args):
    kode = parse_periode(args.bulan)

    def kerja(conn, cfg):
        per = ambil_periode(conn, kode, buat=True)
        wajib_draf(per)
        prorata = terapkan_prorata(conn, per, args.prorata) if args.prorata else []
        with tempfile.TemporaryDirectory(prefix="gaji-umkm-") as tmp:
            hasil, total, pr, sidik = hitung_periode(conn, per, cfg, tmp, args.pph_sementara)
        conn.execute("DELETE FROM hasil WHERE periode_id=? AND revisi=?", (per["id"], per["revisi"]))
        for h in hasil:
            conn.execute("INSERT INTO hasil(periode_id, revisi, karyawan_id, data) VALUES (?,?,?,?)",
                         (per["id"], per["revisi"], h["karyawan_id"], json.dumps(ke_json(h), ensure_ascii=False)))
        conn.execute("INSERT OR REPLACE INTO hasil_periode(periode_id, revisi, dihitung, sidik, total, peringatan) "
                     "VALUES (?,?,?,?,?,?)", (per["id"], per["revisi"], stempel(), sidik,
                                             json.dumps(ke_json(total)), json.dumps(pr, ensure_ascii=False)))
        saran = saran_belum_prorata(conn, per, hasil)
        t = teks_rekap(kode, "draf", per["revisi"], hasil, total, pr, cfg) + "\n\n" + penutup_pembeli(total, hasil)
        return {"periode": kode, "status": "draf", "revisi": per["revisi"], "karyawan": ke_json(hasil),
                "total": ke_json(total), "peringatan_hitung": pr, "tertunda": ke_json(total["tertunda"]),
                "pph_sementara": [h["kode"] for h in hasil if h.get("pph_sementara")],
                "saran_prorata": ke_json(saran), "prorata_diterapkan": ke_json(prorata),
                "bisa_final": not (total["tertunda"] or any(h.get("pph_sementara") for h in hasil)),
                "langkah_berikut": langkah_agent(kode, total, hasil, pr, saran, prorata),
                "ringkasan": {"periode": kode, "karyawan": len(hasil), "tertunda": len(total["tertunda"]),
                              "thp": tc.angka_json(total["take_home_pay"])}}, t
    return jalankan_tulis(args, "hitung", kerja)


def saran_belum_prorata(conn, per, hasil):
    """Karyawan masuk/keluar tengah bulan yang dihitung PENUH (belum ada nominal dibayar): saran prorata kalender."""
    ada = {h["kode"] for h in hasil if "gaji_pokok" not in h["isian"]}
    return [s for s in (saran_prorata(k, per["kode"]) for k in karyawan_periode(conn, per["kode"]) if k["kode"] in ada)
            if s]


def selisih_revisi(lama, baru):
    a = {h["kode"]: h for h in lama["hasil"]}
    b = {h["kode"]: h for h in baru}
    out = []
    for kd in sorted(set(a) | set(b)):
        if kd not in a:
            out.append({"kode": kd, "nama": b[kd]["nama"], "ket": "ditambahkan"})
            continue
        if kd not in b:
            out.append({"kode": kd, "nama": a[kd]["nama"], "ket": "dihapus dari periode"})
            continue
        d = {}
        for kol, jalur in (("gaji_bersih", "take_home_pay"), ("pph21", "pph"), ("biaya_perusahaan", "biaya_perusahaan"),
                           ("total_pendapatan", "total_pendapatan")):
            x, y = D(a[kd]["payroll"][jalur]), D(b[kd]["payroll"][jalur])
            if x != y:
                d[kol] = {"lama": x, "baru": y, "selisih": y - x}
        if d:
            out.append({"kode": kd, "nama": b[kd]["nama"], "ket": "berubah", "rincian": d})
    return out


def teks_selisih(sel):
    if not sel:
        return "Tidak ada angka yang berubah dibanding versi final sebelumnya."
    o = []
    for s in sel:
        if s["ket"] != "berubah":
            o.append("- %s %s: %s" % (s["kode"], s["nama"], s["ket"]))
            continue
        bag = ["%s %s -> %s (%s%s)" % (k.replace("_", " "), rp(v["lama"]), rp(v["baru"]),
                                        "+" if v["selisih"] > 0 else "-", rp(abs(v["selisih"])))
               for k, v in s["rincian"].items()]
        o.append("- %s %s: %s" % (s["kode"], s["nama"], "; ".join(bag)))
    return "\n".join(o)


def cmd_final(args):
    kode = parse_periode(args.bulan)

    def kerja(conn, cfg):
        per = ambil_periode(conn, kode)
        if not per:
            raise Gagal("Periode %s belum ada. Hitung dulu: gaji.py hitung --bulan %s" % (nama_periode(kode), kode))
        wajib_draf(per)
        h = muat_hasil(conn, per)
        if not h:
            raise Gagal("Periode %s belum dihitung. Jalankan: gaji.py hitung --bulan %s" % (nama_periode(kode), kode))
        tertunda = h["total"].get("tertunda") or []
        sementara = [x["nama"] for x in h["hasil"] if x.get("pph_sementara")]
        if tertunda or sementara:
            mtl = "data Januari s.d. bulan lalu untuk Masa Pajak Terakhir belum lengkap"
            bag = ["%s (tertunda: %s)" % (t["nama"], t["alasan"] if t["alasan"] == "data perlu diperbaiki" else mtl)
                   for t in tertunda] + ["%s (PPh 21 masih SEMENTARA: %s)" % (n, mtl) for n in sementara]
            raise Gagal("%s belum bisa dikunci (final) karena: %s. Lengkapi/perbaiki datanya, hitung ulang tanpa angka "
                        "sementara, lalu kunci. Angka karyawan lain tetap bisa diperiksa di rekap draf." % (
                            nama_periode(kode), "; ".join(bag)),
                        tertunda=[t["kode"] for t in tertunda],
                        pph_sementara=[x["kode"] for x in h["hasil"] if x.get("pph_sementara")])
        with tempfile.TemporaryDirectory(prefix="gaji-umkm-") as tmp:
            masukan, _, argv_umum, _ = susun_masukan(conn, per, cfg)
            sidik = hashlib.sha256()
            kel = {}
            for m in masukan:
                kel.setdefault(m["k"]["hari_kerja"], []).append(m)
            for hk in sorted(kel):
                sidik.update(tulis_csv_mesin(os.path.join(tmp, "c.csv"), KOLOM_PAYROLL,
                                             [m["row"] for m in kel[hk]]).encode("utf-8"))
                sidik.update(json.dumps(argv_umum + [str(hk)]).encode("utf-8"))
        if sidik.hexdigest() != h["sidik"]:
            raise Gagal("Data karyawan/komponen/pengaturan berubah sejak periode %s dihitung. Hitung ulang dulu: "
                        "gaji.py hitung --bulan %s, periksa, lalu final lagi." % (nama_periode(kode), kode))
        t = teks_rekap(kode, "final", per["revisi"], h["hasil"], h["total"], h["peringatan"], cfg)
        sel = None
        if per["revisi"] > 0:
            lama = muat_hasil(conn, per, per["revisi"] - 1)
            sel = selisih_revisi(lama, h["hasil"]) if lama else []
            conn.execute("UPDATE revisi SET difinalkan=?, selisih=? WHERE periode_id=? AND nomor=?",
                         (stempel(), json.dumps(ke_json(sel), ensure_ascii=False), per["id"], per["revisi"]))
            t += "\n\nPerubahan dibanding versi final sebelumnya (revisi ke-%d):\n%s" % (per["revisi"] - 1,
                                                                                        teks_selisih(sel))
        conn.execute("UPDATE periode SET status='final', difinalkan=? WHERE id=?", (stempel(), per["id"]))
        t = ("Kunci periode %s. Setelah final, angka tidak bisa diubah kecuali lewat revisi tercatat.\n\n" %
             nama_periode(kode)) + t
        pr = []
        nanti = [r["kode"] for r in conn.execute("SELECT kode FROM periode WHERE kode>? AND kode<=? AND status='final'",
                                                  (kode, kode[:4] + "-12"))]
        if nanti and per["revisi"] > 0:
            pr.append("Periode %s sudah final dan bisa terpengaruh (PPh 21 Desember/bulan keluar memakai data bulan "
                      "ini). Periksa dan revisi bila perlu." % ", ".join(nanti))
        return {"periode": kode, "status": "final", "revisi": per["revisi"], "selisih": ke_json(sel),
                "peringatan": pr, "ringkasan": {"periode": kode, "revisi": per["revisi"]}}, t
    return jalankan_tulis(args, "final", kerja, besar=True, label_backup="final")


def cmd_revisi(args):
    kode = parse_periode(args.bulan)
    alasan = bersih(args.alasan, 300)
    if len(alasan) < 5:
        raise Gagal("Tulis alasan revisi yang jelas, mis. --alasan \"lembur Andi tanggal 12 terlewat\".")

    def kerja(conn, cfg):
        per = ambil_periode(conn, kode)
        if not per or per["status"] != "final":
            raise Gagal("Revisi hanya untuk periode yang sudah final. %s masih draf: ubah langsung lalu hitung ulang."
                        % nama_periode(kode))
        baru = per["revisi"] + 1
        conn.execute("UPDATE periode SET status='draf', revisi=? WHERE id=?", (baru, per["id"]))
        conn.execute("INSERT INTO revisi(periode_id, nomor, dibuka, alasan) VALUES (?,?,?,?)",
                     (per["id"], baru, stempel(), alasan))
        # salin isian? isian tetap (satu set per periode) - hasil lama tetap tersimpan di revisi sebelumnya
        t = ("Buka revisi ke-%d untuk %s. Alasan: %s\nHasil final lama (revisi ke-%d) tetap tersimpan sebagai riwayat. "
             "Setelah itu data bulan ini bisa diubah, dihitung ulang, lalu dikunci lagi." % (
                 baru, nama_periode(kode), alasan, per["revisi"]))
        pr = []
        nanti = [r["kode"] for r in conn.execute("SELECT kode FROM periode WHERE kode>? AND kode<=? AND status='final'",
                                                  (kode, kode[:4] + "-12"))]
        if nanti:
            pr.append("Periode %s sudah final. Bila ada karyawan keluar/Desember di periode itu, PPh 21-nya memakai "
                      "angka bulan ini - periksa setelah revisi selesai." % ", ".join(nanti))
        pr.append("Slip & daftar transfer %s yang sudah dibagikan/diunggah menjadi versi lama. Setelah dikunci lagi, "
                  "slip dibuat ulang; daftar transfer berikutnya berisi SELISIH-nya saja (bisa dibuat penuh bila versi "
                  "lama belum dibayar)." % nama_periode(kode))
        return {"periode": kode, "revisi": baru, "peringatan": pr,
                "langkah_berikut": ["isi --bulan %s ... (ubah data)" % kode, "hitung --bulan %s" % kode,
                                    "final --bulan %s (pratinjau, lalu --ya)" % kode,
                                    "slip --bulan %s; transfer --bulan %s (selisih; --penuh bila versi lama belum "
                                    "dibayar)" % (kode, kode)],
                "ringkasan": {"periode": kode, "revisi": baru, "alasan": alasan}}, t
    return jalankan_tulis(args, "revisi", kerja, besar=True, label_backup="revisi")


def cmd_periode(args):
    def kerja(conn, cfg):
        rows = conn.execute("SELECT * FROM periode ORDER BY kode").fetchall()
        if not rows:
            return {"periode": []}, "Belum ada periode gaji. Mulai: gaji.py hitung --bulan YYYY-MM"
        o, data = ["Periode gaji:"], []
        for p in rows:
            h = muat_hasil(conn, p)
            rv = conn.execute("SELECT * FROM revisi WHERE periode_id=? ORDER BY nomor", (p["id"],)).fetchall()
            status = "FINAL" if p["status"] == "final" else ("DRAF" + (" (sedang revisi)" if p["revisi"] else ""))
            baris = "- %s: %s%s" % (nama_periode(p["kode"]), status,
                                    ", gaji bersih %s, %d karyawan%s" % (
                                        rp(h["total"]["take_home_pay"]), len(h["hasil"]),
                                        ", %d tertunda" % len(h["total"]["tertunda"]) if h["total"].get("tertunda")
                                        else "") if h else ", belum dihitung")
            for r in rv:
                baris += "\n    revisi ke-%d (%s): %s%s" % (r["nomor"], r["dibuka"][:10], r["alasan"],
                                                            "" if r["difinalkan"] else " [belum final]")
            o.append(baris)
            data.append({"kode": p["kode"], "status": p["status"], "revisi": p["revisi"],
                         "revisi_log": [{"nomor": r["nomor"], "alasan": r["alasan"], "dibuka": r["dibuka"],
                                         "difinalkan": r["difinalkan"],
                                         "selisih": json.loads(r["selisih"]) if r["selisih"] else None} for r in rv]})
        return {"periode": data}, "\n".join(o)
    return baca(args, kerja)


def ambil_hasil_wajib(conn, kode):
    per = ambil_periode(conn, kode)
    if not per:
        raise Gagal("Periode %s belum ada. Jalankan: gaji.py hitung --bulan %s" % (nama_periode(kode), kode))
    h = muat_hasil(conn, per)
    if not h:
        if per["revisi"] > 0:
            raise Gagal("%s sedang direvisi dan belum dihitung ulang. Jalankan gaji.py hitung --bulan %s." % (
                nama_periode(kode), kode))
        raise Gagal("Periode %s belum dihitung. Jalankan: gaji.py hitung --bulan %s" % (nama_periode(kode), kode))
    return per, h


def cmd_rekap(args):
    def kerja(conn, cfg):
        if args.tahun:
            return rekap_tahun(conn, cfg, int(args.tahun))
        kode = parse_periode(args.bulan)
        per, h = ambil_hasil_wajib(conn, kode)
        t = teks_rekap(kode, per["status"], per["revisi"], h["hasil"], h["total"], h["peringatan"], cfg)
        return {"periode": kode, "status": per["status"], "revisi": per["revisi"], "total": h["total"],
                "karyawan": [{"kode": x["kode"], "nama": x["nama"], "take_home_pay": x["payroll"]["take_home_pay"],
                              "pph21": x["payroll"]["pph"], "biaya_perusahaan": x["payroll"]["biaya_perusahaan"]}
                             for x in h["hasil"]]}, t
    return baca(args, kerja)


def rekap_tahun(conn, cfg, th):
    rows = conn.execute("SELECT * FROM periode WHERE kode LIKE ? ORDER BY kode", ("%04d-%%" % th,)).fetchall()
    if not rows:
        return {"tahun": th, "bulan": []}, "Belum ada periode gaji tahun %d." % th
    o = ["REKAP GAJI TAHUN %d - %s" % (th, cfg["nama_usaha"] or "(nama usaha)"), "",
         "| Bulan | Status | Karyawan | Gaji bersih | BPJS Kes | BPJS TK | Perkiraan setor PPh 21 | Biaya perusahaan |",
         "|---|---|---:|---:|---:|---:|---:|---:|"]
    jumlah = {k: NOL for k in ("take_home_pay", "setor_bpjs_kesehatan", "setor_bpjs_ketenagakerjaan", "setor_pph21",
                               "biaya_perusahaan")}
    data = []
    for p in rows:
        h = muat_hasil(conn, p)
        if not h:
            o.append("| %s | belum dihitung | | | | | | |" % tc.NAMA_BULAN[int(p["kode"][5:7]) - 1])
            continue
        t = h["total"]
        final = p["status"] == "final"
        o.append("| %s | %s | %d | %s | %s | %s | %s | %s |" % (
            tc.NAMA_BULAN[int(p["kode"][5:7]) - 1], "final" if final else "DRAF", t["jumlah_karyawan"],
            rp(t["take_home_pay"]), rp(t["setor_bpjs_kesehatan"]), rp(t["setor_bpjs_ketenagakerjaan"]),
            rp(t["setor_pph21"]), rp(t["biaya_perusahaan"])))
        if final:
            for k in jumlah:
                jumlah[k] += D(t[k])
        data.append({"kode": p["kode"], "status": p["status"], "total": t})
    o.append("| **Total final** | | | **%s** | **%s** | **%s** | **%s** | **%s** |" % tuple(
        rp(jumlah[k]) for k in ("take_home_pay", "setor_bpjs_kesehatan", "setor_bpjs_ketenagakerjaan", "setor_pph21",
                                "biaya_perusahaan")))
    o += ["", "Total hanya menjumlah periode FINAL.", "", "_" + DISCLAIMER + "_"]
    return {"tahun": th, "bulan": data, "total_final": ke_json(jumlah)}, "\n".join(o)


# --------------------------------------------------------------------------- v1.0.13: hitung cepat (tanpa database)
def pisah_nama_tanggal(teks, opsi):
    if "=" not in str(teks):
        raise Gagal("%s '%s': tulis NAMA=TANGGAL, mis. %s \"Lina=2026-09-14\"" % (opsi, teks, opsi))
    nama, tgl = str(teks).rsplit("=", 1)
    if not nama.strip():
        raise Gagal("%s '%s': nama kosong" % (opsi, teks))
    return nama.strip(), tanggal(tgl, "%s %s" % (opsi, nama.strip())).isoformat()


def pisah_nama_isian(teks, opsi):
    """'Andi: bonus=500rb; kasbon=250rb' -> ('Andi', [('bonus', '500rb'), ('kasbon', '250rb')])."""
    if ":" not in str(teks):
        raise Gagal("%s '%s': tulis NAMA: kolom=nilai; kolom=nilai, mis. %s \"Andi: bonus=500rb; kasbon=250rb\""
                    % (opsi, teks, opsi))
    nama, sisa = str(teks).split(":", 1)
    pasangan = []
    for bag in (b.strip() for b in sisa.split(";")):
        if not bag:
            continue
        if "=" not in bag:
            raise Gagal("%s %s: '%s' harus berbentuk kolom=nilai, mis. bonus=500rb" % (opsi, nama.strip(), bag))
        kol, nilai = bag.split("=", 1)
        pasangan.append((re.sub(r"[\s_]+", "-", kol.strip().lower()), nilai.strip()))
    if not nama.strip() or not pasangan:
        raise Gagal("%s '%s': nama atau komponen kosong" % (opsi, teks))
    return nama.strip(), pasangan


def cari_di_data(conn, nama, opsi):
    """cari_karyawan untuk hitung-cepat: pesan galat menyebut nama yang ada di file (bukan perintah)."""
    try:
        return cari_karyawan(conn, nama)
    except Gagal as e:
        if e.detail.get("pilihan"):
            raise Gagal("%s: %s Tulis nama lengkap atau kodenya." % (opsi, e.pesan.replace(" Ulangi dengan kodenya.", "")),
                        pilihan=e.detail["pilihan"])
        ada = [r["nama"] for r in conn.execute("SELECT nama FROM karyawan ORDER BY kode")]
        raise Gagal("%s: nama '%s' tidak ada di daftar karyawan. Nama yang ada: %s." % (opsi, nama, ", ".join(ada)))


ALASAN_PAGAR = {"tanpa_bpjs_kesehatan": "tidak didaftarkan BPJS Kesehatan",
                "tanpa_bpjs_ketenagakerjaan": "tidak didaftarkan BPJS Ketenagakerjaan",
                "dasar_bpjs_kesehatan_rendah": "dasar iuran BPJS Kesehatan diisi lebih kecil dari upah sebenarnya"}


def pagar_pratinjau(conn, cfg, per):
    """Pagar kepatuhan BPJS yang sama dengan alur database, untuk hitung-cepat (tidak ada yang disimpan).
    Kembalikan {karyawan_id: (karyawan, [kode_masalah], [alasan awam])}."""
    out = {}
    for k in karyawan_periode(conn, per["kode"]):
        isi = isian_karyawan(conn, per, k)
        kd = sorted(masalah_kepatuhan(dict(k), cfg)) + sorted(masalah_dasar_turun(k, isi, per["kode"]))
        if not kd:
            continue
        alasan = [ALASAN_PAGAR[x] for x in kd if x in ALASAN_PAGAR]
        if "dasar_bpjs_turun_bulan_penuh" in kd:
            alasan.append("gaji pokok + tunjangan tetap diisi %s, di bawah data karyawan %s padahal bekerja sebulan "
                          "penuh, jadi dasar iuran BPJS ikut turun" % (
                              rp(D(isi.get("gaji_pokok", k["gaji_pokok"])) +
                                 D(isi.get("tunjangan_tetap", k["tunjangan_tetap"]))),
                              rp(D(k["gaji_pokok"]) + D(k["tunjangan_tetap"]))))
        out[k["id"]] = (k, kd, alasan)
    return out


CATATAN_PAGAR = ("Wajib BPJS dengan upah sebenarnya (UU 24/2011 Pasal 15); boleh hanya dengan alasan sah yang disetujui "
                 "pemilik (mis. iuran lewat sistem lain, cuti di luar tanggungan sesuai perjanjian kerja), bila tidak "
                 "perbaiki datanya.")


def info_pagar(k, kd, alasan, kode):
    inti = "belum dihitung, perlu persetujuan khusus pemilik: %s." % "; ".join(alasan)
    subjek = "%s (%s)" % (k["nama"], k["kode"])
    return {"kode": k["kode"], "nama": k["nama"], "alasan": "perlu persetujuan khusus", "rentang_data": "",
            "tanggal_keluar": "", "bulan_kurang": [], "data_dibutuhkan": alasan, "bisa_pph_sementara": False,
            "sementara_diabaikan": False, "subjek": subjek, "sebab": None, "inti": inti, "tanya_prorata": "",
            "teks": "%s: %s %s" % (subjek, inti, CATATAN_PAGAR), "catatan_pagar": True, "masalah_kepatuhan": kd,
            "saran_prorata": None,
            "langkah_agent": ["Tanyakan alasannya ke pemilik. HANYA bila pemilik sendiri menyetujui dengan alasan sah: "
                              "ulangi hitung-cepat yang sama + --ya-saya-paham --alasan-khusus \"...\" (saat disimpan: "
                              "impor/isi juga dengan --ya-saya-paham). Bila tidak: perbaiki data (kolom bpjs "
                              "kes,tk,jp / hapus gaji-pokok-dibayar) lalu hitung-cepat lagi."]}


ALIAS_SALDO = {"bruto": "bruto", "penghasilan-bruto": "bruto", "pph21": "pph21", "pph-21": "pph21", "pph": "pph21",
               "iuran": "iuran", "jht-jp": "iuran", "iuran-jht-jp": "iuran", "zakat": "zakat"}


def cmd_hitung_cepat(args):
    """Pemakaian pertama: hitung gaji sebulan dari file daftar karyawan TANPA database (tidak ada yang disimpan),
    memakai alur & mesin yang sama dengan `hitung`. Karyawan yang datanya kurang ditandai tertunda."""
    kode = parse_periode(args.bulan)
    th, bl = int(kode[:4]), int(kode[5:7])
    conn = sqlite3.connect(":memory:", isolation_level=None)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(SKEMA_SQL)
        cfg = dict(PENGATURAN_DEFAULT, nama_usaha=bersih(args.nama_usaha or "", 80))
        if args.umk:
            cfg["umk"] = teks_angka(uang(args.umk, "--umk"))
        if args.jkk:
            cfg["jkk"] = teks_angka(persen(args.jkk, "--jkk"))
        if args.batas_jp:
            cfg["batas_jp"] = teks_angka(uang(args.batas_jp, "--batas-jp"))
        conn.executemany("INSERT INTO meta(kunci, nilai) VALUES (?,?)",
                         list(dict(cfg, aplikasi=APLIKASI, skema=str(SKEMA)).items()))
        kepala, rows = baca_tabel(args.data)
        kepala = [ALIAS_IMPOR.get(k, k) for k in kepala]
        if not {"nama", "ptkp", "gaji_pokok"} <= set(kepala):
            raise Gagal("File daftar karyawan wajib punya kolom nama, ptkp (status pajak, mis. TK/0, K/1), dan "
                        "gaji_pokok. Kolom ditemukan: %s" % ", ".join(kepala))
        baru, pr_k, _, galat, tanpa_masuk = impor_baris_karyawan(conn, cfg, rows, "%04d-01-01" % th)
        if galat:
            raise Gagal("Data karyawan perlu diperbaiki dulu (belum ada yang dihitung):\n- " + "\n- ".join(galat),
                        galat=galat)
        for teks in args.masuk or []:
            nama, tgl = pisah_nama_tanggal(teks, "--masuk")
            k = cari_di_data(conn, nama, "Tanggal masuk")
            if k["tanggal_keluar"] and k["tanggal_keluar"] < tgl:
                raise Gagal("%s: tanggal masuk setelah tanggal keluar" % k["nama"])
            conn.execute("UPDATE karyawan SET tanggal_masuk=? WHERE id=?", (tgl, k["id"]))
            tanpa_masuk = [x for x in tanpa_masuk if x != k["nama"]]
        for teks in args.keluar_tgl or []:
            nama, tgl = pisah_nama_tanggal(teks, "--keluar")
            k = cari_di_data(conn, nama, "Tanggal keluar")
            if tgl < k["tanggal_masuk"]:
                raise Gagal("%s: tanggal keluar lebih awal dari tanggal masuk" % k["nama"])
            conn.execute("UPDATE karyawan SET tanggal_keluar=? WHERE id=?", (tgl, k["id"]))
        for teks in args.saldo_awal or []:
            nama, pasangan = pisah_nama_isian(teks, "--saldo-awal")
            k = cari_di_data(conn, nama, "Saldo awal")
            if bl == 1:
                raise Gagal("--saldo-awal tidak dipakai untuk periode Januari (belum ada bulan sebelumnya).")
            nilai = {"bruto": "0", "pph21": "0", "iuran": "0", "zakat": "0"}
            for kol, v in pasangan:
                if kol not in ALIAS_SALDO:
                    raise Gagal("--saldo-awal %s: '%s' tidak dikenal. Pakai bruto=..; pph21=..; iuran=.. [; zakat=..]"
                                % (k["nama"], kol))
                nilai[ALIAS_SALDO[kol]] = teks_angka(uang(v, "--saldo-awal %s %s" % (k["nama"], kol)))
            conn.execute("INSERT OR REPLACE INTO saldo_awal(karyawan_id, tahun, sampai_bulan, bruto, pph21, iuran, "
                         "zakat) VALUES (?,?,?,?,?,?,?)", (k["id"], th, bl - 1, nilai["bruto"], nilai["pph21"],
                                                           nilai["iuran"], nilai["zakat"]))
        per = ambil_periode(conn, kode, buat=True)
        aktif = {k["id"] for k in karyawan_periode(conn, kode)}
        asing = []
        if args.komponen:
            _, _, galat, asing = isi_dari_tabel(conn, per, args.komponen)
            if galat:
                raise Gagal("File komponen perlu diperbaiki dulu:\n- " + "\n- ".join(galat), galat=galat)
        for teks in args.isi or []:
            nama, pasangan = pisah_nama_isian(teks, "--isi")
            k = cari_di_data(conn, nama, "Komponen")
            if k["id"] not in aktif:
                raise Gagal("%s tidak aktif di %s (masuk %s%s)." % (
                    k["nama"], nama_periode(kode), k["tanggal_masuk"],
                    ", keluar " + k["tanggal_keluar"] if k["tanggal_keluar"] else ""))
            for kol, v in pasangan:
                if kol not in OPSI_ISIAN:
                    raise Gagal("--isi %s: komponen '%s' tidak dikenal. Pilihan: %s" % (
                        k["nama"], kol, ", ".join(sorted(OPSI_ISIAN))))
                set_isian(conn, per, k, OPSI_ISIAN[kol], v)
            isi_k = isian_karyawan(conn, per, k)
            if "lembur_rp" in isi_k and ("lembur_hari_kerja" in isi_k or "lembur_hari_libur" in isi_k):
                raise Gagal("%s: isi jam lembur ATAU lembur-rp, jangan keduanya." % k["nama"])
        prorata = terapkan_prorata(conn, per, args.prorata) if args.prorata else []
        # pagar kepatuhan BPJS sama dengan alur database (Aturan wajib 7): tanpa persetujuan khusus pemilik,
        # karyawan itu tertunda (tidak dihitung) - karyawan lain tetap dihitung
        pagar = pagar_pratinjau(conn, cfg, per)
        paham = bool(getattr(args, "ya_saya_paham", False))
        tunda, catat_setuju = {}, []
        for kid, (k, kd, alasan) in pagar.items():
            if paham:
                catat_setuju.append(k["nama"])
            else:
                tunda[kid] = info_pagar(k, kd, alasan, kode)
        with tempfile.TemporaryDirectory(prefix="gaji-umkm-") as tmp:
            hasil, total, pr, _ = hitung_periode(conn, per, cfg, tmp, args.pph_sementara, tunda,
                                                 pratinjau=bersih(getattr(args, "alasan_khusus", "") or "", 200) or True)
        # dasar BPJS turun: keterangan persetujuan (+ alasan) sudah menempel di kalimatnya; kalimat pembuka hanya untuk
        # kepesertaan BPJS (tanpa BPJS / dasar BPJS Kesehatan rendah) supaya tidak diulang dua kali
        kepesertaan = [k["nama"] for k, kd, _ in pagar.values() if set(kd) - {"dasar_bpjs_turun_bulan_penuh"}]
        if catat_setuju and kepesertaan:
            pr = ["PERSETUJUAN KHUSUS pemilik dipakai untuk data BPJS %s%s. Belum disimpan; dicatat saat disimpan." % (
                ", ".join(kepesertaan), " - alasan: %s" % bersih(args.alasan_khusus, 200)
                if getattr(args, "alasan_khusus", None) else "")] + pr
        saran = saran_belum_prorata(conn, per, hasil)
        asumsi = []
        if tanpa_masuk:
            ada = [k["nama"] for k in baru if k["nama"] not in tanpa_masuk]
            if len(tanpa_masuk) == len(baru) and len(baru) > 1:
                siapa = "semua karyawan (%d)" % len(tanpa_masuk)
            elif len(tanpa_masuk) > 3 and len(ada) <= 3:          # jangan daftar belasan nama satu per satu
                siapa = "%d karyawan (semua kecuali %s)" % (len(tanpa_masuk), ", ".join(ada))
            else:
                siapa = ", ".join(tanpa_masuk)
            asumsi.append("Tanggal masuk %s tidak ada di data: dianggap bekerja sejak sebelum %d (bukan karyawan baru). "
                          "Koreksi bila ada yang masuk tahun ini." % (siapa, th))
        if not cfg["umk"]:
            asumsi.append("UMK kota/kabupaten belum disebut: cek upah minimum dan batas bawah iuran BPJS Kesehatan "
                          "dilewati. Sebutkan UMK dari SK Gubernur.")
        # tarif JKK: kalimat sama dengan alur database (peringatan_jkk; hanya karyawan yang DIHITUNG). Bila sebagian
        # atau semua memakai 0,24% karena tarif belum ada, kalimat itu masuk "Asumsi" (bukan diulang di peringatan)
        jkk_data = [x for x in pr if x.startswith("Tarif JKK dari data")]
        if not cfg["jkk"]:
            if jkk_data and "belum diisi untuk" in jkk_data[0]:
                asumsi.append(jkk_data[0])
            elif not jkk_data and any(x.startswith(JKK_BELUM) for x in pr):
                asumsi.append("Tarif JKK belum disebut: dipakai 0,24% (risiko sangat rendah). Ganti sesuai penetapan "
                              "BPJS Ketenagakerjaan usaha Anda.")
        if "bpjs" not in kepala:
            asumsi.append("Data BPJS tidak ada: semua dianggap ikut BPJS Kesehatan, Ketenagakerjaan & Jaminan Pensiun.")
        semua = conn.execute("SELECT * FROM karyawan ORDER BY kode").fetchall()
        hit = {}
        for k in semua:
            hit.setdefault(k["nama"].lower(), []).append(k)
        ganda = [v for v in hit.values() if len(v) > 1]
        if ganda:
            asumsi.append("Nama ganda di data: %s. Pastikan bukan baris dobel; untuk komponen/tanggal sebut kodenya." %
                          "; ".join("%s (%s)" % (v[0]["nama"], ", ".join(x["kode"] for x in v)) for v in ganda))
        if asing:
            asumsi.append(teks_kolom_asing(asing))
        luar = [k["nama"] for k in semua if k["id"] not in aktif]
        if luar:
            asumsi.append("Tidak dihitung karena tanggal masuk/keluarnya di luar %s: %s. Koreksi bila tanggalnya "
                          "keliru." % (nama_periode(kode), ", ".join(luar)))
        file_slip = []
        if args.folder_slip:
            fol = Path(args.folder_slip).expanduser()
            fol.mkdir(parents=True, exist_ok=True)
            for h in hasil:
                kr = conn.execute("SELECT * FROM karyawan WHERE kode=?", (h["kode"],)).fetchone()
                f = fol.resolve() / ("slip-%s-%s-PRATINJAU.md" % (kode, h["kode"]))
                f.write_text(slip_md(h, kode, "pratinjau", 0, cfg, kr) + "\n", encoding="utf-8")
                file_slip.append(str(f))
        t = (teks_rekap(kode, "pratinjau", 0, hasil, total, pr + pr_k, cfg, asumsi) + "\n\n" +
             "Belum disimpan. Bila sudah benar (atau setelah dikoreksi), balas \"simpan\" agar data karyawan & gaji "
             "bulan ini tersimpan di komputer ini.")
        langkah = ["Simpan setelah pemilik setuju: init --nama-usaha .. --ya; atur --umk .. --jkk .. "
                   "[--tanggal-gajian ..]; karyawan impor <file> (pratinjau, lalu --ya; kolom masuk WAJIB di file "
                   "impor - isi tanggal masuk yang benar, yang kosong tadi memakai asumsi 1 Januari); karyawan keluar "
                   "--karyawan <kode> --tanggal .. --ya (untuk --keluar); isi --bulan %s ... (untuk --isi); "
                   "saldo-awal ... (untuk --saldo-awal); hitung --bulan %s [opsi yang sama]" % (kode, kode)]
        langkah += [x for x in langkah_agent(kode, total, hasil, pr, saran, prorata)
                    if not x.startswith(("Slip draf", "Kunci setelah"))]
        return {"ok": True, "mode": "pratinjau", "disimpan": False, "perlu_konfirmasi": True, "periode": kode,
                "bisa_final": False,
                "masalah_kepatuhan": sorted("%s:%s" % (k["kode"], x) for k, kd, _ in pagar.values() for x in kd),
                "perlu_persetujuan_khusus": bool(pagar) and not paham,
                "konfirmasi_kepatuhan": {"karyawan": [k["kode"] for k, _, _ in pagar.values()],
                                         "alasan": bersih(getattr(args, "alasan_khusus", "") or "", 200)}
                if pagar and paham else None,
                "karyawan": ke_json(hasil), "total": ke_json(total), "peringatan_hitung": pr + pr_k,
                "tertunda": ke_json(total["tertunda"]),
                "pph_sementara": [h["kode"] for h in hasil if h.get("pph_sementara")],
                "saran_prorata": ke_json(saran), "prorata_diterapkan": ke_json(prorata), "asumsi": asumsi,
                "kolom_tidak_dikenal": asing,
                "jumlah_karyawan_data": len(semua), "file_slip": file_slip, "langkah_berikut": langkah,
                "teks": t}, t
    finally:
        conn.close()


# --------------------------------------------------------------------------- slip & transfer
def folder_keluaran(args, kode):
    if args.keluar:
        p = Path(args.keluar).expanduser()
    else:
        p = path_db(args).parent / "keluaran" / kode
    p.mkdir(parents=True, exist_ok=True)
    return p.resolve()


def slip_md(h, kode, per_status, revisi, cfg, karyawan_row):
    p = h["payroll"]
    pd, pt, i = p["pendapatan"], p["potongan"], p["iuran"]
    o = []
    if per_status == "pratinjau":
        o.append("> **PRATINJAU (hitung cepat) - belum disimpan dan belum final. Jangan dibagikan.**\n")
    elif per_status != "final":
        o.append("> **DRAF - BELUM FINAL. Jangan dibagikan sebelum periode dikunci.**\n")
    if h.get("pph_sementara"):
        o.append("> **PPh 21 SEMENTARA - perhitungan setahun (Masa Pajak Terakhir) belum final.**\n")
    o += ["# SLIP GAJI - %s" % (cfg["nama_usaha"] or "(nama usaha)"),
          "**Periode:** %s%s  " % (nama_periode(kode), " (revisi ke-%d)" % revisi if revisi else ""),
          "**Nama:** %s (%s)%s  " % (h["nama"], h["kode"], " - " + h["jabatan"] if h["jabatan"] else ""),
          "**Status PTKP:** %s  " % h["ptkp"]]
    if karyawan_row is not None and karyawan_row["nik"]:
        o.append("**NIK:** %s  " % samarkan(karyawan_row["nik"]))
    if karyawan_row is not None and karyawan_row["rekening"]:
        o.append("**Rekening:** %s %s  " % (karyawan_row["bank"], samarkan(karyawan_row["rekening"])))
    o += ["", "| Pendapatan | Jumlah |", "|---|---:|"]
    for k, v in pd.items():
        if D(v) or k == "Gaji pokok":
            o.append("| %s | %s |" % (k, rp(v)))
    o += ["| **Total pendapatan** | **%s** |" % rp(p["total_pendapatan"]), "", "| Potongan | Jumlah |", "|---|---:|"]
    for k, v in pt.items():
        if k == "Potongan lain":
            if D(h["potongan_tidak_masuk"]):
                o.append("| Potongan tidak masuk | %s |" % rp(h["potongan_tidak_masuk"]))
            if D(h["potongan_lain_saja"]):
                o.append("| Potongan lain (kasbon, dll.) | %s |" % rp(h["potongan_lain_saja"]))
            continue
        if D(v):
            o.append("| %s | %s |" % (k, rp(v)))
    o += ["| **Total potongan** | **%s** |" % rp(p["total_potongan"]), "",
          "### GAJI BERSIH (TAKE HOME PAY): %s" % rp(p["take_home_pay"]), "",
          "_Ditanggung perusahaan (tidak memotong gaji): BPJS Kesehatan 4%% %s, JHT 3,7%% %s, JKK %s%% %s, JKM 0,3%% %s, "
          "JP 2%% %s._" % (rp(i["kes_perusahaan"]), rp(i["jht_perusahaan"]),
                           str(p["jkk_persen"]).replace(".", ","), rp(i["jkk"]), rp(i["jkm"]), rp(i["jp_perusahaan"]))]
    info = p["pph_info"]
    if info["masa_terakhir"]:
        d = info["detail"]
        o.append("_PPh 21: dihitung ulang setahun (Masa Pajak Terakhir - %s): PPh setahun %s dikurangi yang sudah "
                 "dipotong %s._" % (h["masa_terakhir"]["alasan"] if h.get("masa_terakhir") else "",
                                    rp(d["pph_terutang"]), rp(d["pph_sudah_dipotong"])))
    else:
        o.append("_PPh 21: TER kategori %s %s%% x penghasilan bruto pajak %s (termasuk premi JKK, JKM, BPJS Kesehatan "
                 "bagian perusahaan)._" % (info["kategori"], str(info["tarif"]).replace(".", ","), rp(info["bruto"])))
    if h.get("pph_sementara"):
        mtt = h.get("masa_terakhir_tertunda") or {}
        o.append("_PPh 21 SEMENTARA: bulan ini %s adalah Masa Pajak Terakhir, tetapi data %s belum ada, jadi PPh 21 "
                 "dihitung dengan tarif efektif bulanan (TER) saja. Perhitungan setahun belum final dan wajib dilengkapi "
                 "sebelum bukti potong 1721-A1 (BPA1) dibuat; PPh 21 dan gaji bersih bisa berubah._" % (
                     h["nama"], mtt.get("rentang_data", "Januari s.d. bulan lalu")))
    if p["dtp"]:
        o.append("_PPh 21 Ditanggung Pemerintah (PMK 105/2025): PPh 21 %s tetap dipotong, lalu %s dibayar tunai kembali "
                 "bersama gaji, jadi gaji bersih tidak berkurang karena pajak. Setoran PPh 21 ke negara untuk karyawan "
                 "ini: %s._" % (rp(p["potongan"]["PPh 21"]), rp(p["pendapatan"]["PPh 21 DTP dibayar tunai"]),
                                rp(p["pph_disetor"])))
    if p.get("lembur"):
        o.append("_Lembur: upah sejam = 1/173 x %s (PP 35/2021)._" % rp(p["lembur"]["dasar_upah"]))
    o += ["", "_" + DISCLAIMER + "_"]
    return "\n".join(o)


def cmd_slip(args):
    kode = parse_periode(args.bulan)

    def kerja(conn, cfg):
        per, h = ambil_hasil_wajib(conn, kode)
        hasil = h["hasil"]
        if args.karyawan:
            k = cari_karyawan(conn, args.karyawan)
            hasil = [x for x in hasil if x["kode"] == k["kode"]]
            tunda = [t for t in (h["total"].get("tertunda") or []) if t["kode"] == k["kode"]]
            if not hasil and tunda:
                raise Gagal("Slip %s belum bisa dibuat karena masih tertunda. %s" % (k["nama"], tunda[0]["teks"]),
                            tertunda=[k["kode"]])
            if not hasil:
                raise Gagal("%s tidak ada di periode %s." % (k["nama"], nama_periode(kode)))
        fol = folder_keluaran(args, kode)
        file = []
        semua = []
        for x in hasil:
            kr = conn.execute("SELECT * FROM karyawan WHERE kode=?", (x["kode"],)).fetchone()
            isi = slip_md(x, kode, per["status"], per["revisi"], cfg, kr)
            nama_file = "slip-%s-%s%s%s.md" % (kode, x["kode"], "-rev%d" % per["revisi"] if per["revisi"] else "",
                                               "-DRAF" if per["status"] != "final" else "")
            (fol / nama_file).write_text(isi + "\n", encoding="utf-8")
            file.append(str(fol / nama_file))
            semua.append(isi)
        t = "Slip %s %s (%d file):\n%s" % (nama_periode(kode), "FINAL" if per["status"] == "final" else "DRAF",
                                           len(file), "\n".join("- " + Path(f).name for f in file))
        if args.karyawan:
            t += "\n\n" + semua[0]
        t += "\n\nSlip berisi gaji pribadi: kirim ke masing-masing karyawan saja, jangan ke grup."
        return {"periode": kode, "status": per["status"], "file": file}, t
    return baca(args, kerja)


def cmd_transfer(args):
    kode = parse_periode(args.bulan)

    def kerja(conn, cfg):
        per, h = ambil_hasil_wajib(conn, kode)
        if per["status"] != "final":
            raise Gagal("Daftar transfer hanya dibuat untuk periode FINAL (agar tidak membayar angka draf). Kunci dulu: "
                        "gaji.py final --bulan %s" % kode)
        fol = folder_keluaran(args, kode)
        pr, rows, total, tanpa, langkah = [], [], NOL, [], []
        selisih = per["revisi"] > 0 and not args.penuh
        lama = {}
        if selisih:
            hl = muat_hasil(conn, per, per["revisi"] - 1)
            lama = {x["kode"]: D(x["payroll"]["take_home_pay"]) for x in hl["hasil"]} if hl else {}
            pr.append("Periode ini revisi ke-%d: daftar hanya berisi SELISIH gaji bersih dibanding versi final "
                      "sebelumnya (dianggap sudah dibayar). Bila versi lama belum pernah dibayar, daftar bisa dibuat "
                      "ulang berisi gaji penuh." % per["revisi"])
            langkah.append("Versi lama belum dibayar: transfer --bulan %s --penuh" % kode)
        nama = fol / ("transfer-%s-%s%s.csv" % ("selisih" if selisih else "gaji", kode,
                                                "-rev%d" % per["revisi"] if per["revisi"] else ""))
        for x in h["hasil"]:
            kr = conn.execute("SELECT * FROM karyawan WHERE kode=?", (x["kode"],)).fetchone()
            thp = D(x["payroll"]["take_home_pay"])
            if selisih:
                beda = thp - lama.get(x["kode"], NOL)
                if beda < 0:
                    pr.append("%s: gaji bersih turun %s dibanding versi lama (kelebihan bayar). Tidak ditransfer; "
                              "selesaikan sesuai kesepakatan dengan karyawan." % (x["nama"], rp(-beda)))
                    continue
                if beda == 0:
                    continue
                thp = beda
            if thp <= 0:
                pr.append("%s: gaji bersih %s (tidak ditransfer)." % (x["nama"], rp(thp)))
                continue
            if not kr["rekening"]:
                tanpa.append("%s %s" % (x["nama"], rp(thp)))
                continue
            rek = kr["rekening"] if args.rekening_lengkap else samarkan(kr["rekening"])
            rows.append([len(rows) + 1, x["kode"], kr["atas_nama"] or x["nama"], kr["bank"], rek, teks_angka(thp),
                         ("Kekurangan gaji %s (revisi %d)" if selisih else "Gaji %s") % (
                             (nama_periode(kode), per["revisi"]) if selisih else nama_periode(kode))])
            total += thp
        with open(nama, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=args.pemisah)
            w.writerow(["no", "kode", "nama_penerima", "bank", "no_rekening", "nominal", "keterangan"])
            w.writerows(rows)
        if tanpa:
            pr.append("Belum ada nomor rekening (bayar tunai, atau sebutkan nomor rekeningnya): %s" % "; ".join(tanpa))
            langkah.append("Isi rekening: karyawan ubah --karyawan <kode> --bank .. --rekening .. (pratinjau, lalu --ya)")
        if args.rekening_lengkap:
            pr.append("File ini berisi nomor rekening LENGKAP. Simpan di komputer ini saja, unggah sendiri ke internet "
                      "banking, lalu hapus/simpan aman. Jangan dikirim lewat chat.")
        else:
            pr.append("Nomor rekening di file disamarkan. Untuk unggah ke bank, isi nomor lengkap di aplikasi bank, atau "
                      "minta file berisi nomor lengkap (hanya disimpan di komputer ini, tidak ditampilkan di chat).")
            langkah.append("Bila pemilik minta nomor lengkap untuk unggah ke bank: transfer --bulan %s "
                           "--rekening-lengkap" % kode)
        pr.append("Format kolom tiap bank berbeda: sesuaikan dengan template unggah massal bank Anda. Tidak ada "
                  "koneksi ke bank; periksa total sebelum menyetujui transfer.")
        t = "Daftar transfer %s: %d penerima, total %s (file daftar transfer sudah dibuat)" % (
            nama_periode(kode), len(rows), rp(total))
        return {"periode": kode, "file": str(nama), "jumlah": len(rows), "total": tc.angka_json(total),
                "peringatan": pr, "langkah_berikut": langkah}, t + "\n\n" + "\n".join("Catatan: " + p for p in pr)
    return baca(args, kerja)


# --------------------------------------------------------------------------- THR (hitung-thr)
def cmd_thr(args):
    kode = parse_periode(args.bulan)

    def kerja(conn, cfg):
        per = ambil_periode(conn, kode, buat=True)
        wajib_draf(per)
        daftar = karyawan_periode(conn, kode)
        if args.karyawan:
            pilih = {cari_karyawan(conn, x)["id"] for x in args.karyawan}
            daftar = [k for k in daftar if k["id"] in pilih]
        if not daftar:
            raise Gagal("Tidak ada karyawan aktif di %s." % nama_periode(kode))
        kol = ["nama", "jabatan", "jenis", "ptkp", "gaji_pokok", "tunjangan_tetap", "tanggal_mulai", "tanggal_berhenti"]
        rows = [{"nama": k["nama"], "jabatan": k["jabatan"], "jenis": k["jenis"], "ptkp": k["ptkp"],
                 "gaji_pokok": k["gaji_pokok"], "tunjangan_tetap": k["tunjangan_tetap"],
                 "tanggal_mulai": k["tanggal_masuk"], "tanggal_berhenti": k["tanggal_keluar"]} for k in daftar]
        with tempfile.TemporaryDirectory(prefix="gaji-umkm-") as tmp:
            f = os.path.join(tmp, "thr.csv")
            tulis_csv_mesin(f, kol, rows)
            argv = ["--data", f, "--hari-raya", args.hari_raya, "--nama-hari-raya",
                    re.sub(r"[;,]", " ", args.nama_hari_raya), "--format", "json", "--hari-ini", hari_ini().isoformat()]
            if args.tanggal_bayar:
                argv += ["--tanggal-bayar", args.tanggal_bayar]
            out = jalankan_mesin("thr.py", argv)
        byr = date.fromisoformat(out["tanggal_bayar"])
        if byr.strftime("%Y-%m") != kode:
            raise Gagal("Tanggal bayar THR %s tidak berada di periode %s. Pakai --bulan %s atau --tanggal-bayar di "
                        "bulan ini." % (ftgl(byr), nama_periode(kode), byr.strftime("%Y-%m")))
        baris, pr = [], []
        for k, x in zip(daftar, out["karyawan"]):
            if not x["berhak"] or not D(x["thr"]):
                baris.append("- %s: tidak berhak (%s)" % (k["nama"], x.get("alasan") or "-"))
                set_isian(conn, per, k, "thr", "-")
                continue
            set_isian(conn, per, k, "thr", teks_angka(D(x["thr"])), "THR %s (hitung-thr): %s" % (
                args.nama_hari_raya, x["rumus"]))
            baris.append("- %s: %s (%s; masa kerja %s bulan; dasar %s)" % (k["nama"], rp(x["thr"]), x["rumus"],
                                                                         x["masa_kerja_bulan"], x["dasar_upah"]))
            pr += [p for p in x.get("peringatan", []) if "PPh 21" not in p]
        pr += out.get("peringatan_umum", [])
        pr.append("PPh 21 atas THR dihitung saat gaji %s dihitung (THR digabung ke penghasilan bulan itu, cara "
                  "slip-gaji-bpjs), bukan angka PPh di hitung-thr." % nama_periode(kode))
        t = ("THR %s - hari raya %s, batas bayar %s, rencana bayar %s (masuk gaji %s):\n%s\nTotal THR: %s" % (
            args.nama_hari_raya, ftgl(date.fromisoformat(out["hari_raya"])),
            ftgl(date.fromisoformat(out["batas_bayar"])), ftgl(byr), nama_periode(kode), "\n".join(baris),
            rp(out["total"]["thr"])))
        return {"periode": kode, "thr": out, "peringatan": pr, "pengumuman": out.get("pengumuman", ""),
                "ringkasan": {"periode": kode, "total_thr": out["total"]["thr"]}}, t
    return jalankan_tulis(args, "thr", kerja, besar=True, label_backup="thr")


# --------------------------------------------------------------------------- cek PPh 21 setahun (pph21-ter)
def cmd_pph21_tahunan(args):
    th = int(args.tahun)

    def kerja(conn, cfg):
        kary = conn.execute("SELECT * FROM karyawan ORDER BY kode").fetchall()
        if args.karyawan:
            kk = cari_karyawan(conn, args.karyawan)
            kary = [kk]
        per = {p["kode"]: p for p in conn.execute("SELECT * FROM periode WHERE kode LIKE ? AND status='final'",
                                                   ("%04d-%%" % th,))}
        o = ["CEK PPh 21 TAHUN %d (dihitung ulang terpisah dengan mesin pph21-ter)" % th, "",
             "| Kode | Nama | Bulan | Total bruto | PPh 21 di aplikasi | PPh 21 menurut pph21-ter | Hasil |",
             "|---|---|---|---:|---:|---:|---|"]
        data, ada_selisih = [], False
        with tempfile.TemporaryDirectory(prefix="gaji-umkm-") as tmp:
            for k in kary:
                bulan = []
                for kp in sorted(per):
                    h = conn.execute("SELECT data FROM hasil WHERE periode_id=? AND revisi=? AND karyawan_id=?",
                                     (per[kp]["id"], per[kp]["revisi"], k["id"])).fetchone()
                    if h:
                        bulan.append((int(kp[5:7]), json.loads(h["data"])))
                sa = conn.execute("SELECT * FROM saldo_awal WHERE karyawan_id=? AND tahun=?", (k["id"], th)).fetchone()
                if not bulan:
                    continue
                masuk = date.fromisoformat(k["tanggal_masuk"])
                bm = masuk.month if masuk.year == th else 1
                akhir = bulan[-1][0]
                rows = []
                if sa:
                    rows.append({"bulan": sa["sampai_bulan"], "bruto": sa["bruto"], "iuran_pensiun": sa["iuran"],
                                 "zakat": sa["zakat"], "pph_dipotong": sa["pph21"]})
                for b, x in bulan:
                    p = x["payroll"]
                    rows.append({"bulan": b, "bruto": teks_angka(D(p["pph_info"]["bruto"])),
                                 "iuran_pensiun": teks_angka(D(p["iuran"]["jht_karyawan"]) + D(p["iuran"]["jp_karyawan"])),
                                 "zakat": teks_angka(D(p["potongan"]["Zakat"])), "pph_dipotong": ""})
                harap = list(range((sa["sampai_bulan"] + 1) if sa else bm, akhir + 1))
                kurang = [b for b in harap if b not in [x[0] for x in bulan]]
                pph_app = sum((D(x["payroll"]["pph"]) for _, x in bulan), NOL) + (D(sa["pph21"]) if sa else NOL)
                bruto_tot = sum((D(r["bruto"]) for r in rows), NOL)
                if kurang:
                    o.append("| %s | %s | %s | %s | %s | - | data belum lengkap (%s belum final) |" % (
                        k["kode"], k["nama"], "%d-%d" % (bm, akhir), rp(bruto_tot), rp(pph_app),
                        ", ".join(tc.NAMA_BULAN[b - 1] for b in kurang)))
                    data.append({"kode": k["kode"], "status": "belum_lengkap", "bulan_kurang": kurang})
                    continue
                f = os.path.join(tmp, "p-%s.csv" % k["kode"])
                tulis_csv_mesin(f, ["bulan", "bruto", "iuran_pensiun", "zakat", "pph_dipotong"], rows)
                keluar_th = k["tanggal_keluar"] and k["tanggal_keluar"][:7] == "%04d-%02d" % (th, akhir)
                ptkp = bulan[-1][1]["ptkp"]
                argv = ["setahun", "--ptkp", ptkp, "--data", f, "--mulai", str(min(r["bulan"] for r in rows)),
                        "--akhir", str(akhir), "--status", "berhenti" if keluar_th else "aktif", "--tahun", str(th),
                        "--jumlah-bulan", str(akhir - bm + 1), "--format", "json"]
                out = jalankan_mesin("pph21.py", argv)
                pph_cek = D(out["ringkasan"]["pph21_terutang_setahun"])
                cocok = pph_cek == pph_app
                ada_selisih |= not cocok
                ket = "cocok" if cocok else "SELISIH %s" % rp(pph_app - pph_cek)
                if not out.get("masa_terakhir"):
                    ket += " (tahun berjalan, belum Masa Pajak Terakhir)"
                o.append("| %s | %s | %s-%s | %s | %s | %s | %s |" % (
                    k["kode"], k["nama"], tc.NAMA_BULAN[bm - 1][:3], tc.NAMA_BULAN[akhir - 1][:3],
                    rp(out["ringkasan"]["total_bruto"]), rp(pph_app), rp(pph_cek), ket))
                data.append({"kode": k["kode"], "status": "cocok" if cocok else "selisih", "pph_aplikasi": pph_app,
                             "pph_pph21_ter": pph_cek, "masa_terakhir": bool(out.get("masa_terakhir")),
                             "total_bruto": out["ringkasan"]["total_bruto"]})
        if not data:
            return {"tahun": th, "karyawan": []}, "Belum ada periode FINAL di tahun %d." % th
        o += ["", "Angka ini bahan bukti potong tahunan (BPA1) - buat & laporkan di Coretax." if not ada_selisih else
              "Ada SELISIH: jangan buat bukti potong dulu; periksa periode yang direvisi/saldo awal, atau tanyakan ke "
              "konsultan pajak.", "", "_" + DISCLAIMER + "_"]
        return {"tahun": th, "karyawan": ke_json(data), "ada_selisih": ada_selisih}, "\n".join(o)
    return baca(args, kerja)


# --------------------------------------------------------------------------- pengingat
def geser_akhir_pekan(d):
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


def tanggal_gajian(cfg, th, bl):
    akhir = calendar.monthrange(th, bl)[1]
    s = str(cfg.get("tanggal_gajian") or "25").strip().lower()
    if s == "akhir":
        return date(th, bl, akhir)
    return date(th, bl, min(int(s), akhir))


def cmd_pengingat(args):
    rentang = int(args.rentang)
    if not 0 <= rentang <= 60:
        raise Gagal("--rentang harus 0-60 hari")

    def kerja(conn, cfg):
        h0 = hari_ini()
        h1 = h0 + timedelta(days=rentang)
        acara = []
        bulan = []
        d = date(h0.year, h0.month, 1) - timedelta(days=1)
        d = date(d.year, d.month, 1)
        while d <= h1:
            bulan.append((d.year, d.month))
            d = (d + timedelta(days=32)).replace(day=1)

        def info_periode(kp):
            p = ambil_periode(conn, kp)
            if not p:
                return None, "periode %s belum dihitung" % nama_periode(kp)
            h = muat_hasil(conn, p)
            if not h:
                return None, "periode %s belum dihitung" % nama_periode(kp)
            if p["status"] != "final":
                return h["total"], "periode %s masih DRAF" % nama_periode(kp)
            return h["total"], "periode %s final" % nama_periode(kp)

        for th, bl in bulan:
            kp = "%04d-%02d" % (th, bl)
            berikut = (date(th, bl, 1) + timedelta(days=32)).replace(day=1)
            tg = tanggal_gajian(cfg, th, bl)
            if h0 <= tg <= h1:
                tot, st = info_periode(kp)
                acara.append((tg, "Gajian %s: %s%s" % (nama_periode(kp), st, ", gaji bersih %s" % rp(
                    tot["take_home_pay"]) if tot else "")))
            kes = date(th, bl, 10)
            if h0 <= kes <= h1:
                tot, st = info_periode("%04d-%02d" % ((kes - timedelta(days=15)).year, (kes - timedelta(days=15)).month))
                acara.append((kes, "Batas setor iuran BPJS Kesehatan (tgl 10 setiap bulan, Perpres 82/2018 Pasal 39)%s"
                              % (": perkiraan %s dari %s" % (rp(tot["setor_bpjs_kesehatan"]), st) if tot else
                                 " (%s)" % st)))
            # JP: tgl 15 bulan berikutnya TANPA pergeseran (PP 45/2015 Pasal 30 ayat (3)).
            # JHT/JKK/JKM: tgl 15, bila hari libur -> hari kerja berikutnya (PP 46/2015 Pasal 19 ayat (2)-(3);
            # PP 44/2015 Pasal 21 ayat (2)-(3)). Iuran ditagih bersama, jadi pengingat utama = tgl 15 persis.
            tk15 = date(berikut.year, berikut.month, 15)
            tk = geser_akhir_pekan(tk15)
            if h0 <= tk15 <= h1 or h0 <= tk <= h1:
                tot, st = info_periode(kp)
                jml = (": %s (%s)" % (rp(tot["setor_bpjs_ketenagakerjaan"]), st)) if tot else " (%s)" % st
                ada_jp = (not tot) or D(tot.get("jp_perusahaan")) + D(tot.get("jp_karyawan")) > 0
                if tk == tk15 or not ada_jp:
                    if h0 <= tk <= h1:
                        acara.append((tk, "Batas setor iuran BPJS Ketenagakerjaan masa %s (JHT, JKK, JKM%s: tgl 15 "
                                      "bulan berikutnya; PP 44/2015 Pasal 21, PP 46/2015 Pasal 19, PP 45/2015 Pasal 30)%s"
                                      % (nama_periode(kp), ", JP" if ada_jp else "", jml)))
                else:
                    if h0 <= tk15 <= h1:
                        acara.append((tk15, "Batas setor iuran JP (Jaminan Pensiun) masa %s: tgl 15 bulan berikutnya, "
                                      "TIDAK digeser walau hari libur (PP 45/2015 Pasal 30 ayat (3)). Iuran BPJS "
                                      "Ketenagakerjaan ditagih bersama - paling aman bayar semuanya paling lambat "
                                      "tanggal ini atau hari kerja sebelumnya%s" % (nama_periode(kp), jml)))
                    if h0 <= tk <= h1:
                        acara.append((tk, "Batas setor iuran JHT, JKK, JKM masa %s (tgl 15 jatuh hari libur -> hari kerja "
                                      "berikutnya; PP 46/2015 Pasal 19, PP 44/2015 Pasal 21). JP sudah jatuh tempo "
                                      "tgl 15." % nama_periode(kp)))
            pph = geser_akhir_pekan(date(berikut.year, berikut.month, 15))
            if h0 <= pph <= h1:
                tot, st = info_periode(kp)
                acara.append((pph, "Batas setor PPh 21 masa %s (tgl 15 bulan berikutnya, PMK 81/2024)%s" % (
                    nama_periode(kp), ": %s (%s)" % (rp(tot["setor_pph21"]), st) if tot else " (%s)" % st)))
            lap = geser_akhir_pekan(date(berikut.year, berikut.month, 20))
            if h0 <= lap <= h1:
                acara.append((lap, "Batas lapor SPT Masa PPh 21 masa %s (tgl 20 bulan berikutnya, PMK 81/2024)" %
                              nama_periode(kp)))
        acara.sort(key=lambda x: x[0])
        judul = "PENGINGAT GAJI & SETORAN %s - %s s.d. %s" % (cfg["nama_usaha"] or "", ftgl(h0), ftgl(h1))
        if not acara:
            t = "%s\nTidak ada tenggat gaji/setoran dalam %d hari ke depan." % (judul, rentang)
        else:
            t = judul + "\n" + "\n".join("- %s %s: %s" % (["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"][d.weekday()],
                                                          ftgl(d), x) for d, x in acara)
            t += ("\nTanggal yang jatuh di Sabtu/Minggu sudah digeser ke Senin (tidak berlaku untuk BPJS Kesehatan dan "
                  "JP). "
                  "Libur nasional/cuti bersama TIDAK dicek - lihat skill kalender-pajak. Angka = total perusahaan, "
                  "tanpa data pribadi karyawan.")
        return {"acara": [{"tanggal": d.isoformat(), "teks": x} for d, x in acara]}, t
    return baca(args, kerja)


# --------------------------------------------------------------------------- init, atur, info, backup, restore
def cmd_init(args):
    db = path_db(args)
    if db.exists():
        raise Gagal("Database sudah ada di %s. Tidak dibuat ulang (data aman). Lihat: gaji.py info" % db)
    t = ("Siapkan penyimpanan data gaji%s di komputer ini.\nData gaji & karyawan hanya disimpan di komputer ini "
         "(tidak dikirim ke mana pun) dan dicadangkan otomatis." % (" untuk %s" % args.nama_usaha
                                                                    if args.nama_usaha else ""))
    if not args.ya:
        t = "PRATINJAU (belum disimpan):\n" + t + "\n\n" + penutup_pratinjau("init")
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "db": str(db), "teks": t,
                "langkah_berikut": [LANGKAH_SIMPAN]}, t
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db))
    try:
        conn.executescript(SKEMA_SQL)
        meta = dict(PENGATURAN_DEFAULT, aplikasi=APLIKASI, skema=str(SKEMA), versi=VERSI, dibuat=stempel(),
                    nama_usaha=bersih(args.nama_usaha or "", 80))
        conn.executemany("INSERT INTO meta(kunci, nilai) VALUES (?,?)", list(meta.items()))
        conn.commit()
    finally:
        conn.close()
    t = "TERSIMPAN. " + t + "\nBerikutnya: UMK & tarif JKK usaha Anda, lalu data karyawan."
    return {"ok": True, "mode": "tersimpan", "db": str(db), "teks": t,
            "langkah_berikut": ["atur --umk .. --jkk .. [--tanggal-gajian ..]", "karyawan impor <file> / karyawan tambah"]}, t


def cmd_atur(args):
    def kerja(conn, cfg):
        ubah = {}
        if args.nama_usaha is not None:
            ubah["nama_usaha"] = bersih(args.nama_usaha, 80)
        if args.umk is not None:
            ubah["umk"] = "" if args.umk == "-" else teks_angka(uang(args.umk, "--umk"))
        if args.jkk is not None:
            ubah["jkk"] = "" if args.jkk == "-" else teks_angka(persen(args.jkk, "--jkk"))
        if args.batas_jp is not None:
            ubah["batas_jp"] = "" if args.batas_jp == "-" else teks_angka(uang(args.batas_jp, "--batas-jp"))
        if args.tanggal_gajian is not None:
            s = args.tanggal_gajian.strip().lower()
            if s != "akhir" and not (s.isdigit() and 1 <= int(s) <= 31):
                raise Gagal("--tanggal-gajian harus 1-31 atau 'akhir'")
            ubah["tanggal_gajian"] = s
        if args.potongan_per_hari_alpa is not None:
            if args.potongan_per_hari_alpa == "-":
                ubah["potongan_per_hari_alpa"], ubah["dasar_potongan"] = "", ""
            else:
                dasar = bersih(args.dasar_potongan or cfg["dasar_potongan"], 120)
                if len(dasar) < 5:
                    raise Gagal("Potongan tidak masuk hanya sah bila diatur di Perjanjian Kerja/Peraturan Perusahaan/PKB. "
                                "Sebutkan dasarnya: --dasar-potongan \"Peraturan Perusahaan Pasal 12\".")
                ubah["potongan_per_hari_alpa"] = teks_angka(uang(args.potongan_per_hari_alpa, "--potongan-per-hari-alpa"))
                ubah["dasar_potongan"] = dasar
        if not ubah:
            raise Gagal("Tidak ada yang diatur. Opsi: --nama-usaha, --umk, --jkk, --batas-jp, --tanggal-gajian, "
                        "--potongan-per-hari-alpa + --dasar-potongan")
        for k, v in ubah.items():
            conn.execute("INSERT OR REPLACE INTO meta(kunci, nilai) VALUES (?,?)", (k, v))
        t = "Pengaturan disimpan: " + ", ".join("%s = %s" % (k, v or "(kosong)") for k, v in ubah.items())
        pr = []
        if "umk" in ubah and ubah["umk"]:
            pr.append("UMK diisi dari data Anda (SK Gubernur). Skill tidak menyimpan angka UMK resmi.")
        draf = [r["kode"] for r in conn.execute("SELECT kode FROM periode WHERE status='draf'")]
        if draf:
            pr.append("Hitung ulang periode draf (%s) agar memakai pengaturan baru." % ", ".join(draf))
        return {"diubah": ubah, "peringatan": pr, "ringkasan": ubah}, t
    return jalankan_tulis(args, "atur", kerja)


def cmd_info(args):
    db = path_db(args)
    manifest = cek_mesin()
    mesin = ", ".join("%s (%s %s)" % (n, i["skill_sumber"], i["versi_skill_sumber"]) for n, i in manifest["file"].items())
    if not db.exists():
        t = ("Database gaji belum ada (akan dibuat di %s). Mulai: gaji.py init --nama-usaha \"...\" (pratinjau, lalu "
             "--ya).\nMesin hitung: %s, aturan per %s." % (db, mesin, manifest["tanggal_aturan"]))
        return {"ok": True, "mode": "baca", "db": str(db), "ada": False, "teks": t}, t

    def kerja(conn, cfg):
        nk = conn.execute("SELECT COUNT(*) FROM karyawan").fetchone()[0]
        per = conn.execute("SELECT kode, status, revisi FROM periode ORDER BY kode DESC LIMIT 6").fetchall()
        cek = conn.execute("PRAGMA quick_check").fetchone()[0]
        bks = sorted(folder_backup(db).glob("gaji-*.db")) if folder_backup(db).is_dir() else []
        t = ("Database: %s (pemeriksaan: %s)\nUsaha: %s | karyawan terdaftar: %d\nUMK: %s | JKK default: %s | batas JP: "
             "%s | tanggal gajian: %s | potongan alpa: %s\nPeriode terakhir: %s\nCadangan: %d file di %s\nMesin hitung: "
             "%s, aturan per %s." % (
                 db, cek, cfg["nama_usaha"] or "-", nk, rp(cfg["umk"]) if cfg["umk"] else "belum diisi",
                 (cfg["jkk"].replace(".", ",") + "%") if cfg["jkk"] else "0,24% (default slip-gaji-bpjs)",
                 rp(cfg["batas_jp"]) if cfg["batas_jp"] else "otomatis (slip-gaji-bpjs)", cfg["tanggal_gajian"],
                 "%s/hari (%s)" % (rp(cfg["potongan_per_hari_alpa"]), cfg["dasar_potongan"])
                 if cfg["potongan_per_hari_alpa"] else "tidak dipotong otomatis",
                 ", ".join("%s %s%s" % (p["kode"], p["status"], " rev%d" % p["revisi"] if p["revisi"] else "")
                           for p in per) or "-", len(bks), folder_backup(db), mesin, manifest["tanggal_aturan"]))
        return {"ada": True, "db": str(db), "pengaturan": cfg, "karyawan": nk, "pemeriksaan": cek,
                "jumlah_backup": len(bks)}, t
    return baca(args, kerja)


def cmd_backup(args):
    db = path_db(args)
    fol = folder_backup(db)
    if args.daftar:
        bks = sorted(fol.glob("gaji-*.db")) if fol.is_dir() else []
        if bks:
            t = ("Cadangan di %s (terbaru paling bawah):\n%s\nPulihkan: gaji.py restore --dari \"%s\" (pratinjau, lalu "
                 "--ya)." % (fol, "\n".join("- " + str(b) for b in bks[-30:]), bks[-1]))
        else:
            t = "Belum ada cadangan di %s." % fol
        return {"ok": True, "mode": "baca", "folder": str(fol), "backup": [str(b) for b in bks], "teks": t}, t
    conn = buka(db, baca_saja=True)
    conn.close()
    b = buat_backup(db, re.sub(r"[^\w-]", "", args.label or "manual") or "manual")
    t = "Cadangan dibuat: %s\nSimpan salinannya juga di flashdisk/penyimpanan lain (berisi data gaji pribadi)." % b
    return {"ok": True, "mode": "tersimpan", "backup": b, "teks": t}, t


def status_db(db):
    if not db.exists():
        return "tidak_ada"
    try:
        c = buka(db, baca_saja=True)
    except Gagal as e:
        if e.detail.get("rusak"):
            return "rusak"
        raise
    try:
        cek = c.execute("PRAGMA quick_check").fetchone()[0]
    except sqlite3.DatabaseError:
        cek = "rusak"
    finally:
        c.close()
    return "sehat" if cek == "ok" else "rusak"


def cmd_restore(args):
    """Pulihkan dari cadangan: periksa cadangan -> simpan database aktif ke backup-gaji -> salin ke file sementara ->
    periksa -> os.replace (atomik). Tidak pernah menghapus database lama."""
    db = path_db(args)
    src = Path(args.dari).expanduser().resolve()
    if not src.is_file():
        raise Gagal("File cadangan %s tidak ada. Lihat daftar: gaji.py backup --daftar" % src)
    if src == db:
        raise Gagal("File cadangan sama dengan database aktif. Pilih file dari gaji.py backup --daftar.")
    try:
        c = buka(src, baca_saja=True)
    except Gagal as e:
        raise Gagal("File cadangan %s tidak bisa dipakai (%s). Pilih cadangan lain." % (src.name, e.pesan.split(". ")[0]))
    try:
        nk = c.execute("SELECT COUNT(*) FROM karyawan").fetchone()[0]
        np_ = c.execute("SELECT COUNT(*) FROM periode").fetchone()[0]
        cek = c.execute("PRAGMA quick_check").fetchone()[0]
    finally:
        c.close()
    if cek != "ok":
        raise Gagal("File cadangan %s juga bermasalah (%s). Pilih cadangan lain." % (src.name, cek))
    try:
        st = status_db(db)
    except Gagal as e:
        if "sedang dipakai" in e.pesan:
            raise
        raise Gagal("File %s bukan database gaji-umkm; restore dibatalkan agar file itu tidak tertimpa." % db)
    nasib = {"tidak_ada": "Database belum ada; cadangan akan dipasang di lokasi itu.",
             "sehat": "Database saat ini disalin dulu apa adanya ke folder backup-gaji.",
             "rusak": "Database saat ini RUSAK; file itu dipindah (tidak dihapus) ke folder backup-gaji."}[st]
    if not args.ya:
        t = ("PRATINJAU (belum disimpan):\nDatabase %s akan diganti dengan cadangan %s (%d karyawan, %d periode). %s\n"
             "Perubahan setelah waktu cadangan itu akan hilang dari database aktif (tetap ada di salinan).\n\n%s"
             % (db, src, nk, np_, nasib, penutup_pratinjau("restore")))
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "status_db": st, "teks": t,
                "langkah_berikut": [LANGKAH_SIMPAN]}, t
    db.parent.mkdir(parents=True, exist_ok=True)
    fol = folder_backup(db)
    fol.mkdir(parents=True, exist_ok=True)
    tmp = nama_unik(db.parent, ".gaji-restore-%d" % os.getpid(), ".tmp")
    simpanan = None
    try:
        s_, d_ = sqlite3.connect(str(src)), sqlite3.connect(str(tmp))
        try:
            s_.backup(d_)
        finally:
            d_.close()
            s_.close()
        c = sqlite3.connect(str(tmp))
        try:
            ok = c.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
        finally:
            c.close()
        if not ok or ok[0] != APLIKASI:
            raise Gagal("Salinan cadangan tidak valid; database aktif tidak diubah.")
        waktu = datetime.now().strftime("%Y%m%d-%H%M%S")
        if st == "sehat":
            c = sqlite3.connect(str(db), timeout=10, isolation_level=None)
            try:
                c.execute("BEGIN IMMEDIATE")
                c.execute("ROLLBACK")
            except sqlite3.OperationalError as e:
                if _terkunci(e):
                    raise Gagal(PESAN_TERKUNCI)
                raise
            finally:
                c.close()
            simpanan = nama_unik(fol, "gaji-%s-sebelum-restore" % waktu)
            simpanan.write_bytes(db.read_bytes())
        elif st == "rusak":
            simpanan = nama_unik(fol, "rusak-gaji-%s" % waktu)
            os.replace(str(db), str(simpanan))
            for ek in ("-journal", "-wal", "-shm"):
                j = Path(str(db) + ek)
                if j.exists():
                    os.replace(str(j), str(simpanan) + ek)
        os.replace(str(tmp), str(db))
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
    t = "TERSIMPAN. Database %s dipulihkan dari %s (%d karyawan, %d periode)." % (db, src, nk, np_)
    if simpanan:
        t += "\n%s: %s" % ("File rusak dipindah (tidak dihapus) ke" if st == "rusak" else "Salinan database sebelumnya",
                           simpanan)
    return {"ok": True, "mode": "tersimpan", "backup": str(simpanan) if simpanan else None, "teks": t}, t


# --------------------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print("GAGAL: perintah tidak lengkap/salah: %s. Lihat --help." % message, file=sys.stderr)
        sys.exit(2)


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    umum.add_argument("--db", help="File database (default ~/KomunitechData/gaji/gaji.db; ENV KOMUNITECH_GAJI_DB)")
    umum.add_argument("--json", action="store_true", help="Output JSON (untuk agent)")
    umum.add_argument("--hari-ini", help=argparse.SUPPRESS)
    tulis = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    tulis.add_argument("--ya", action="store_true", help="Simpan perubahan besar (tanpa ini hanya pratinjau)")
    kel = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    kel.add_argument("--keluar", help="Folder file keluaran (default: keluaran/<periode> di sebelah database)")

    p = ParserID(prog="gaji.py", description="Penggajian bulanan lokal UMKM (gaji-umkm %s)" % VERSI, allow_abbrev=False)
    p.add_argument("--versi", action="version", version="gaji-umkm " + VERSI)
    sub = p.add_subparsers(dest="perintah", parser_class=ParserID)
    sub.required = True

    s = sub.add_parser("init", parents=[umum, tulis], help="Buat database baru", allow_abbrev=False)
    s.add_argument("--nama-usaha")
    sub.add_parser("info", parents=[umum], help="Lokasi database, pengaturan, pemeriksaan", allow_abbrev=False)
    s = sub.add_parser("atur", parents=[umum], help="Pengaturan usaha", allow_abbrev=False)
    for o in ("nama-usaha", "umk", "jkk", "batas-jp", "tanggal-gajian", "potongan-per-hari-alpa", "dasar-potongan"):
        s.add_argument("--" + o)

    s = sub.add_parser("karyawan", help="Data karyawan: tambah/ubah/daftar/impor", allow_abbrev=False)
    ks = s.add_subparsers(dest="aksi", parser_class=ParserID)
    ks.required = True
    opsi_k = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    for o in ("nama", "jabatan", "jenis", "ptkp", "gaji-pokok", "tunjangan-tetap", "tunjangan-tidak-tetap", "zakat",
              "bpjs", "jkk", "hari-kerja", "dasar-bpjs-kesehatan", "dtp", "bruto-tetap-januari", "nik", "bank",
              "rekening", "atas-nama", "kode-absensi", "masuk"):
        opsi_k.add_argument("--" + o)
    paham = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    paham.add_argument(FLAG_PAHAM, dest="ya_saya_paham", action="store_true",
                       help="Persetujuan khusus pemilik untuk data yang tidak sesuai kewajiban BPJS (dicatat di log)")
    paham.add_argument("--alasan-khusus", help="Alasan persetujuan khusus (dicatat di log)")
    a = ks.add_parser("tambah", parents=[umum, tulis, opsi_k, paham], help="Tambah karyawan", allow_abbrev=False)
    a.add_argument("--kode")
    a = ks.add_parser("ubah", parents=[umum, tulis, opsi_k, paham], help="Ubah data karyawan / catat keluar", allow_abbrev=False)
    a.add_argument("--karyawan", required=True)
    a.add_argument("--keluar", help="Tanggal keluar/berhenti (YYYY-MM-DD; '-' batal)")
    a = ks.add_parser("keluar", parents=[umum, tulis, paham], help="Catat karyawan berhenti", allow_abbrev=False)
    a.add_argument("--karyawan", required=True)
    a.add_argument("--tanggal", required=True)
    a = ks.add_parser("daftar", parents=[umum], help="Daftar karyawan (NIK/rekening disamarkan)", allow_abbrev=False)
    a.add_argument("--semua", action="store_true", help="Termasuk yang sudah keluar")
    a = ks.add_parser("impor", parents=[umum, tulis, paham], help="Impor dari CSV", allow_abbrev=False)
    a.add_argument("file")

    s = sub.add_parser("isi", parents=[umum, tulis, paham], help="Isi komponen tidak tetap/penyesuaian satu periode", allow_abbrev=False)
    s.add_argument("--bulan", required=True)
    s.add_argument("--karyawan")
    s.add_argument("--file", help="CSV banyak karyawan (kolom kode/nama + komponen)")
    for kol in ISIAN:
        if kol in ("gaji_pokok", "tunjangan_tetap"):
            continue
        s.add_argument("--" + kol.replace("_", "-"), dest=kol)
    s.add_argument("--kasbon")
    s.add_argument("--gaji-pokok-dibayar")
    s.add_argument("--tunjangan-tetap-dibayar")
    s.add_argument("--keterangan")

    s = sub.add_parser("impor-absensi", parents=[umum, tulis], help="Impor CSV rekap dari skill absensi-lokal", allow_abbrev=False)
    s.add_argument("file")
    s.add_argument("--bulan", required=True)

    s = sub.add_parser("saldo-awal", parents=[umum], help="PPh/bruto Januari s.d. sebelum memakai aplikasi", allow_abbrev=False)
    s.add_argument("--karyawan", required=True)
    s.add_argument("--tahun", required=True, type=int)
    s.add_argument("--sampai-bulan", required=True, type=int)
    for o in ("bruto", "pph21", "iuran", "zakat"):
        s.add_argument("--" + o)
    s.add_argument("--hapus", action="store_true")

    s = sub.add_parser("hitung", parents=[umum], help="Hitung massal satu periode (draf)", allow_abbrev=False)
    s.add_argument("--bulan", required=True)
    s.add_argument("--pph-sementara", action="store_true",
                   help="Karyawan keluar (Masa Pajak Terakhir) tanpa data Januari s.d. bulan lalu: hitung bulan ini "
                        "saja dengan TER, ditandai SEMENTARA (default: tertunda, tidak dihitung)")
    s.add_argument("--prorata", choices=["kalender", "penuh"],
                   help="Masuk/keluar tengah bulan tanpa nominal dibayar: kalender = gaji pokok & tunjangan tetap x "
                        "hari bekerja / hari dalam bulan; penuh = hapus prorata otomatis (default: tidak diubah)")
    s = sub.add_parser("hitung-cepat", parents=[umum, paham], help="Pemakaian pertama: hitung sebulan dari file karyawan "
                       "TANPA database (tidak ada yang disimpan; --db diabaikan)", allow_abbrev=False)
    s.add_argument("--data", required=True, help="CSV daftar karyawan (kolom seperti karyawan impor; masuk opsional)")
    s.add_argument("--bulan", required=True)
    for o in ("nama-usaha", "umk", "jkk", "batas-jp"):
        s.add_argument("--" + o)
    s.add_argument("--isi", action="append", help="NAMA: kolom=nilai; kolom=nilai (mis. \"Andi: bonus=500rb; kasbon=250rb\")")
    s.add_argument("--komponen", help="CSV komponen (format isi --file)")
    s.add_argument("--masuk", action="append", help="NAMA=YYYY-MM-DD (tanggal masuk)")
    s.add_argument("--keluar", dest="keluar_tgl", action="append", help="NAMA=YYYY-MM-DD (tanggal keluar/terakhir kerja)")
    s.add_argument("--saldo-awal", action="append",
                   help="NAMA: bruto=..; pph21=..; iuran=.. (total Januari/bulan masuk s.d. bulan lalu)")
    s.add_argument("--pph-sementara", action="store_true")
    s.add_argument("--prorata", choices=["kalender", "penuh"])
    s.add_argument("--folder-slip", help="Folder untuk file slip PRATINJAU (opsional)")
    s = sub.add_parser("final", parents=[umum, tulis], help="Kunci periode", allow_abbrev=False)
    s.add_argument("--bulan", required=True)
    s = sub.add_parser("revisi", parents=[umum, tulis], help="Buka revisi tercatat untuk periode final", allow_abbrev=False)
    s.add_argument("--bulan", required=True)
    s.add_argument("--alasan", required=True)
    sub.add_parser("periode", parents=[umum], help="Daftar periode & riwayat revisi", allow_abbrev=False)
    s = sub.add_parser("rekap", parents=[umum], help="Rekap perusahaan satu periode atau setahun", allow_abbrev=False)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--bulan")
    g.add_argument("--tahun")
    s = sub.add_parser("slip", parents=[umum, kel], help="Slip per karyawan (Markdown)", allow_abbrev=False)
    s.add_argument("--bulan", required=True)
    s.add_argument("--karyawan")
    s = sub.add_parser("transfer", parents=[umum, kel], help="Daftar transfer CSV (periode final)", allow_abbrev=False)
    s.add_argument("--bulan", required=True)
    s.add_argument("--pemisah", choices=[";", ","], default=";")
    s.add_argument("--penuh", action="store_true", help="Periode revisi: tulis gaji bersih penuh, bukan selisih")
    s.add_argument("--rekening-lengkap", action="store_true",
                   help="Tulis nomor rekening lengkap HANYA di file CSV (tidak pernah ditampilkan)")
    s = sub.add_parser("thr", parents=[umum, tulis], help="Hitung THR (mesin hitung-thr) dan masukkan ke periode", allow_abbrev=False)
    s.add_argument("--bulan", required=True)
    s.add_argument("--hari-raya", required=True)
    s.add_argument("--nama-hari-raya", default="Hari Raya Keagamaan")
    s.add_argument("--tanggal-bayar")
    s.add_argument("--karyawan", action="append")
    s = sub.add_parser("pph21-tahunan", parents=[umum], help="Cek PPh 21 setahun dengan mesin pph21-ter", allow_abbrev=False)
    s.add_argument("--tahun", required=True)
    s.add_argument("--karyawan")
    s = sub.add_parser("pengingat", parents=[umum], help="Tenggat gajian & setoran N hari ke depan (hanya baca)", allow_abbrev=False)
    s.add_argument("--rentang", default="3")
    s = sub.add_parser("backup", parents=[umum], help="Buat/daftar cadangan", allow_abbrev=False)
    s.add_argument("--daftar", action="store_true")
    s.add_argument("--label")
    s = sub.add_parser("restore", parents=[umum, tulis], help="Pulihkan dari cadangan", allow_abbrev=False)
    s.add_argument("--dari", required=True)
    return p


def jalankan(args):
    if getattr(args, "hari_ini", None):
        _JAM["hari_ini"] = tanggal(args.hari_ini, "--hari-ini")
    p = args.perintah
    if p == "karyawan":
        if args.aksi == "keluar":
            args.keluar = args.tanggal
            for o in ("nama", "jabatan", "jenis", "ptkp", "gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap",
                      "zakat", "bpjs", "jkk", "hari_kerja", "dasar_bpjs_kesehatan", "dtp", "bruto_tetap_januari", "nik",
                      "bank", "rekening", "atas_nama", "kode_absensi", "masuk"):
                setattr(args, o, None)
            return cmd_karyawan_ubah(args)
        return {"tambah": cmd_karyawan_tambah, "ubah": cmd_karyawan_ubah, "daftar": cmd_karyawan_daftar,
                "impor": cmd_karyawan_impor}[args.aksi](args)
    if p == "isi" and not args.file and not args.karyawan:
        raise Gagal("Sebutkan --karyawan (atau --file untuk banyak karyawan).")
    return {"init": cmd_init, "info": cmd_info, "atur": cmd_atur, "isi": cmd_isi, "impor-absensi": cmd_impor_absensi,
            "saldo-awal": cmd_saldo_awal, "hitung": cmd_hitung, "hitung-cepat": cmd_hitung_cepat,
            "final": cmd_final, "revisi": cmd_revisi,
            "periode": cmd_periode, "rekap": cmd_rekap, "slip": cmd_slip, "transfer": cmd_transfer, "thr": cmd_thr,
            "pph21-tahunan": cmd_pph21_tahunan, "pengingat": cmd_pengingat, "backup": cmd_backup,
            "restore": cmd_restore}[p](args)


BATAS_PESAN = 3800        # satu pesan Telegram maks. 4.096 karakter; sisakan ruang untuk sapaan/pertanyaan agent


def bagi_teks(teks, maks=BATAS_PESAN):
    """Teks pemilik yang terlalu panjang untuk satu pesan chat -> beberapa bagian <= maks, dipotong di batas bagian
    (baris kosong), lalu di batas baris (mis. tabel karyawan yang panjang; judul kolom tabel diulang di bagian
    berikutnya), baru di batas kata. Judul rekap tidak dibiarkan sendirian (bila bagian berikutnya tidak muat
    bersamanya, bagian itu dipotong per baris), dan bagian terakhir yang sangat pendek (mis. hanya kalimat penutup)
    diberi bagian sebelumnya (mis. disclaimer). Tidak ada isi yang dibuang atau diubah."""
    if len(teks) <= maks:
        return [teks]
    bagian, cur = [], ""
    pendek = maks // 4

    def tambah(potongan, sambung):
        nonlocal cur
        if cur and len(cur) + len(sambung) + len(potongan) <= maks:
            cur += sambung + potongan
            return True
        if not cur and len(potongan) <= maks:
            cur = potongan
            return True
        return False

    for blok in teks.split("\n\n"):
        if tambah(blok, "\n\n"):
            continue
        if len(blok) <= maks and len(cur) >= pendek:      # bagian utuh muat di pesan berikutnya
            bagian.append(cur)
            cur = blok
            continue
        barisan = blok.split("\n")                         # terlalu panjang / bagian sebelumnya terlalu pendek
        kepala = barisan[:2] if len(barisan) > 2 and barisan[0].startswith("|") and barisan[1].startswith("|---") \
            else []
        for n, baris in enumerate(barisan):
            while len(baris) > maks:                       # satu baris sangat panjang: potong di spasi
                i = baris.rfind(" ", 0, maks)
                i = i if i > 0 else maks
                if cur:
                    bagian.append(cur)
                bagian.append(baris[:i])
                cur, baris = "", baris[i:].lstrip(" ")
            if tambah(baris, "\n" if n else "\n\n"):
                continue
            bagian.append(cur)
            cur = "\n".join(kepala + [baris]) if kepala and n >= 2 and baris.startswith("|") else baris
    if cur:
        bagian.append(cur)
    # bagian terakhir sangat pendek: pindahkan bagian (blok) terakhir dari pesan sebelumnya ke sana bila muat
    while len(bagian) >= 2 and len(bagian[-1]) < pendek and "\n\n" in bagian[-2]:
        kepala_, blok = bagian[-2].rsplit("\n\n", 1)
        if len(blok) + 2 + len(bagian[-1]) > maks or len(kepala_) < pendek:
            break
        bagian[-2], bagian[-1] = kepala_, blok + "\n\n" + bagian[-1]
    return bagian


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        data, teks = jalankan(args)
        kode = 0
    except Gagal as e:
        data = {"ok": False, "error": e.pesan}
        data.update(ke_json(e.detail))
        teks = "GAGAL: " + e.pesan
        kode = 1
    except sqlite3.OperationalError as e:
        data = {"ok": False, "error": PESAN_TERKUNCI if _terkunci(e) else "Kesalahan database: %s" % e}
        teks = "GAGAL: " + data["error"]
        kode = 1
    if isinstance(data.get("teks"), str) and len(data["teks"]) > BATAS_PESAN:
        data["teks_bagian"] = bagi_teks(data["teks"])      # kirim sebagai beberapa pesan berurutan (lihat SKILL.md)
    if args.json:
        print(json.dumps(ke_json(data), ensure_ascii=False, indent=2))
    else:
        print(teks, file=sys.stdout if kode == 0 else sys.stderr)
    return kode


if __name__ == "__main__":
    for s_ in (sys.stdout, sys.stderr):
        try:
            s_.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
