#!/usr/bin/env python3
"""Laporan harian/mingguan gabungan untuk pemilik usaha (laporan-harian-usaha 1.1.0).

Menggabungkan data dari alat lokal Komunitech yang terpasang di komputer yang sama:
  kasir-lokal (penjualan), buku-stok (stok), absensi-lokal (kehadiran),
  pengingat-follow-up (tagihan & follow-up), crm-wa (prospek/pipeline penjualan).
Alat yang tidak ada dilewati dengan catatan, bukan error.

HANYA MEMBACA. Cara kerjanya (tahan perubahan skema):
  1. Database alat dibuka read-only (URI `file:...?mode=ro`, dengan batas tunggu) lalu disalin ke
     folder sementara ("snapshot") dengan `VACUUM INTO`. File asli tidak pernah ditulis.
  2. Perintah laporan RESMI tiap alat (`kasir.py rekap --json`, `stok.py laporan ringkas --json`,
     `absensi.py harian/rekap --json`, `cek_jatuh_tempo.py rekap`, `crm.py rekap --json`) dijalankan
     lewat subprocess terhadap snapshot itu. Angka dihitung oleh alatnya sendiri, jadi laporan tetap
     benar bila tabel internal alat berubah (termasuk migrasi otomatis buku-stok, yang hanya terjadi
     di snapshot).
  3. Hanya dua hal yang tidak tersedia di perintah resmi dibaca langsung dari snapshot, dengan
     pengecekan kolom lebih dulu: selisih kas saat tutup kasir (tabel `sesi` kasir) dan apakah nota
     kasir sudah diimpor ke buku-stok (tabel `pesanan`). Jika kolomnya berubah, bagian itu dilewati
     dengan catatan.

Hanya library standar Python 3.8+. Tanpa jaringan. Lintas OS (Windows: `python`/`py`).

Contoh:
  python3 laporan.py                        # laporan harian hari ini (WIB), teks siap Telegram
  python3 laporan.py --tanggal kemarin
  python3 laporan.py --periode mingguan     # minggu lalu (Senin-Minggu) dibanding minggu sebelumnya
  python3 laporan.py --json --samarkan

Kode keluar: 0 = laporan dibuat (termasuk bila sebagian/semua alat belum ada); 2 = argumen salah.
"""
import argparse
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

VERSI = "1.1.0"
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
# Indonesia tidak memakai jam musim panas, jadi offset tetap ini persis.
TZ_TETAP = {"asia/jakarta": (7, "WIB"), "wib": (7, "WIB"), "asia/pontianak": (7, "WIB"),
            "asia/makassar": (8, "WITA"), "wita": (8, "WITA"),
            "asia/jayapura": (9, "WIT"), "wit": (9, "WIT")}
NAMA_TZ = {7: "Asia/Jakarta", 8: "Asia/Makassar", 9: "Asia/Jayapura"}
ALAT = {
    "kasir": {"skill": "kasir-lokal", "script": "kasir.py"},
    "stok": {"skill": "buku-stok", "script": "stok.py"},
    "absensi": {"skill": "absensi-lokal", "script": "absensi.py"},
    "pengingat": {"skill": "pengingat-follow-up", "script": "cek_jatuh_tempo.py"},
    "crm": {"skill": "crm-wa", "script": "crm.py"},
}


class ArgSalah(Exception):
    pass


class GagalAlat(Exception):
    pass


# --------------------------------------------------------------------------- format
def rp(n):
    n = int(n)
    return ("-" if n < 0 else "") + "Rp " + "{:,}".format(abs(n)).replace(",", ".")


def fq(x):
    """Jumlah barang gaya Indonesia: 2 / 1,5."""
    try:
        d = Decimal(str(x))
    except Exception:
        return str(x)
    if d == d.to_integral_value():
        return "{:,}".format(int(d)).replace(",", ".")
    return str(d.normalize()).replace(".", ",")


def tgl_id(d, hari=True):
    t = "%d %s %d" % (d.day, BULAN[d.month], d.year)
    return ("%s, %s" % (HARI[d.weekday()], t)) if hari else t


def tgl_pendek(d):
    return "%s %d/%d" % (HARI[d.weekday()][:3], d.day, d.month)


def persen(kini, lalu, satuan="Rp 0"):
    """Perubahan persen = (kini - lalu) / lalu x 100, dibulatkan 1 desimal (0,05 ke atas menjauhi nol).

    Mengembalikan (angka_persen_str_atau_None, teks). Pembagi nol/minus tidak dihitung. `satuan` hanya mengubah
    teks untuk kasus pembanding nol (default "Rp 0"; dipakai "0" polos untuk jumlah bukan rupiah, mis. prospek)."""
    if kini is None or lalu is None:
        return None, "tidak ada data pembanding"
    if lalu == 0:
        if kini == 0:
            return None, "sama-sama %s" % satuan
        return None, "naik dari %s (persen tidak dihitung)" % satuan
    if lalu < 0:
        return None, "persen tidak dihitung (pembanding minus)"
    p = (Decimal(kini - lalu) * 100 / Decimal(lalu)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    s = str(abs(p)).replace(".", ",")
    if p > 0:
        return str(p), "naik %s%%" % s
    if p < 0:
        return str(p), "turun %s%%" % s
    return "0.0", "sama (0%)"


def inisial(nama):
    nama = str(nama or "").strip()
    return (nama[0].upper() + ".") if nama else "?"


# --------------------------------------------------------------------------- waktu
def zona(tz_nama):
    k = (tz_nama or "Asia/Jakarta").strip().lower()
    if k in TZ_TETAP:
        jam, label = TZ_TETAP[k]
        return timezone(timedelta(hours=jam)), label, NAMA_TZ[jam]
    # Sengaja dibatasi ke zona Indonesia saja (bukan zona IANA sembarang): kasir/absensi/laporan ini untuk
    # usaha di Indonesia, dan zona di luar itu tidak berguna serta pernah lolos tanpa peringatan (cacat).
    raise ArgSalah("zona waktu '%s' tidak dikenal atau di luar Indonesia. Pakai Asia/Jakarta (WIB), Asia/Makassar "
                   "(WITA), atau Asia/Jayapura (WIT)." % tz_nama)


def waktu_sekarang(args, tz):
    if args.sekarang:
        s = args.sekarang.strip().replace(" ", "T")
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            w = datetime.fromisoformat(s)
        except ValueError:
            raise ArgSalah("--sekarang '%s' tidak valid. Contoh: 2026-09-24T21:00+07:00" % args.sekarang)
        if w.tzinfo is None:
            w = w.replace(tzinfo=tz)
        return w.astimezone(tz)
    return datetime.now(timezone.utc).astimezone(tz)


def baca_tanggal(teks, hari_ini):
    t = (teks or "hari-ini").strip().lower().replace(" ", "-")
    if t in ("hari-ini", "hariini", "today"):
        return hari_ini
    if t in ("kemarin", "yesterday"):
        return hari_ini - timedelta(days=1)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", t)
        if not m:
            raise ArgSalah("tanggal '%s' tidak dikenali. Pakai hari-ini, kemarin, 2026-09-24, atau 24/09/2026." % teks)
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        return date(y, mo, d)
    except ValueError:
        raise ArgSalah("tanggal '%s' tidak ada di kalender." % teks)


def tentukan_periode(args, hari_ini):
    """harian: D vs D-1 & D-7. mingguan: Senin-Minggu vs minggu sebelumnya."""
    if args.periode == "harian":
        d = baca_tanggal(args.tanggal, hari_ini)
        if d > hari_ini:
            raise ArgSalah("tanggal %s belum terjadi (hari ini %s)." % (d.isoformat(), hari_ini.isoformat()))
        return {"jenis": "harian", "dari": d, "sampai": d,
                "banding": [("kemarin", d - timedelta(days=1), d - timedelta(days=1)),
                            ("minggu_lalu", d - timedelta(days=7), d - timedelta(days=7))]}
    if args.tanggal:
        acuan = baca_tanggal(args.tanggal, hari_ini)
        senin = acuan - timedelta(days=acuan.weekday())
    else:  # minggu lalu yang sudah selesai
        senin = hari_ini - timedelta(days=hari_ini.weekday() + 7)
    if senin > hari_ini:
        raise ArgSalah("minggu itu belum dimulai.")
    minggu = senin + timedelta(days=6)
    berjalan = minggu > hari_ini
    if berjalan:  # minggu berjalan: sampai hari ini, dibanding hari yang sama minggu sebelumnya (adil)
        minggu = hari_ini
    return {"jenis": "mingguan", "dari": senin, "sampai": minggu, "berjalan": berjalan,
            "banding": [("minggu_sebelumnya", senin - timedelta(days=7), minggu - timedelta(days=7))]}


# --------------------------------------------------------------------------- lokasi alat
def path_db_default(nama):
    """Sama persis dengan urutan di script masing-masing alat (tanpa --db)."""
    env_file = {"kasir": "KOMUNITECH_KASIR_DB", "stok": "KOMUNITECH_STOK_DB", "absensi": "KOMUNITECH_ABSENSI_DB",
                "crm": "KOMUNITECH_CRM_DB"}[nama]
    if os.environ.get(env_file):
        return Path(os.environ[env_file]).expanduser()
    sub = {"kasir": Path("kasir") / "kasir.db", "stok": Path("stok.db"), "absensi": Path("absensi") / "absensi.db",
           "crm": Path("crm") / "crm.db"}[nama]
    if os.environ.get("KOMUNITECH_DATA"):
        return Path(os.environ["KOMUNITECH_DATA"]).expanduser() / sub
    return Path.home() / "KomunitechData" / sub


def kandidat_pengingat():
    c = [Path.cwd() / "pengingat" / "DAFTAR.csv",
         Path.home() / ".openclaw" / "workspace" / "pengingat" / "DAFTAR.csv"]
    if os.environ.get("KOMUNITECH_DATA"):
        c.append(Path(os.environ["KOMUNITECH_DATA"]).expanduser() / "pengingat" / "DAFTAR.csv")
    c.append(Path.home() / "KomunitechData" / "pengingat" / "DAFTAR.csv")
    return c


def folder_skills():
    sini = Path(__file__).resolve().parent.parent.parent  # folder tempat skill-skill terpasang
    home, cwd = Path.home(), Path.cwd()
    daftar = [sini, home / ".openclaw" / "skills", home / ".claude" / "skills", home / ".agents" / "skills",
              home / ".cursor" / "skills", home / ".openclaw" / "workspace" / "skills",
              cwd / "skills", cwd / ".claude" / "skills", cwd / ".agents" / "skills", cwd / ".cursor" / "skills"]
    hasil = []
    for p in daftar:
        if p not in hasil:
            hasil.append(p)
    return hasil


def cari_script(nama, override):
    if override:
        p = Path(override).expanduser()
        return p if p.is_file() else None
    info = ALAT[nama]
    for fol in folder_skills():
        p = fol / info["skill"] / "scripts" / info["script"]
        if p.is_file():
            return p
    return None


# --------------------------------------------------------------------------- baca aman
def snapshot(src, tujuan, timeout):
    """Salin database ke `tujuan` lewat koneksi read-only. File asli tidak pernah ditulis."""
    uri = Path(src).resolve().as_uri() + "?mode=ro"
    try:
        con = sqlite3.connect(uri, uri=True, timeout=timeout)
    except sqlite3.Error as e:
        raise GagalAlat("database tidak bisa dibuka (%s)" % e)
    try:
        try:
            con.execute("SELECT count(*) FROM sqlite_master").fetchone()
            con.execute("VACUUM INTO ?", (str(tujuan),))
        except sqlite3.OperationalError as e:
            s = str(e).lower()
            if "locked" in s or "busy" in s:
                raise GagalAlat("database sedang dipakai program lain lebih dari %s detik (mis. transaksi sedang "
                                "disimpan). Data aman; jalankan laporan lagi sebentar lagi." % fq(timeout))
            if "syntax" in s or "vacuum" in s:  # SQLite < 3.27: salin dengan backup API di dalam kunci baca
                con.execute("BEGIN")
                con.execute("SELECT count(*) FROM sqlite_master").fetchone()
                dst = sqlite3.connect(str(tujuan))
                try:
                    con.backup(dst)
                finally:
                    dst.close()
                con.execute("COMMIT")
            else:
                raise GagalAlat("database tidak bisa dibaca (%s)" % e)
        except sqlite3.DatabaseError as e:
            raise GagalAlat("file bukan database atau rusak (%s). Pulihkan dari folder backup alatnya." % e)
    finally:
        con.close()


def jalankan(script, argv, timeout):
    env = {k: v for k, v in os.environ.items() if not k.startswith("KOMUNITECH_")}
    env["PYTHONIOENCODING"] = "utf-8"
    env["KOMUNITECH_KASIR_TIMEOUT"] = str(max(1, int(timeout)))
    try:
        p = subprocess.run([sys.executable, str(script)] + argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=max(30, timeout * 4), env=env, cwd=str(Path(script).parent))
    except subprocess.TimeoutExpired:
        raise GagalAlat("alat tidak merespons (waktu habis)")
    except OSError as e:
        raise GagalAlat("alat tidak bisa dijalankan (%s)" % e)
    out = p.stdout.decode("utf-8", "replace").strip()
    err = p.stderr.decode("utf-8", "replace").strip()
    data = None
    if out:
        try:
            data = json.loads(out)
        except ValueError:
            data = None
    if p.returncode == 2 and data is None:
        raise GagalAlat("versi alat tidak cocok (perintah ditolak: %s)" % (err.splitlines()[-1] if err else "?"))
    if isinstance(data, dict) and data.get("ok") is False:
        raise GagalAlat(str(data.get("error") or "alat melaporkan gagal"))
    if p.returncode != 0:
        pesan = err.splitlines()[-1] if err else "kode keluar %d" % p.returncode
        raise GagalAlat(pesan.replace("ERROR: ", ""))
    if not isinstance(data, dict):
        raise GagalAlat("keluaran alat tidak dikenali (versi alat berbeda?)")
    return data


def kolom_ada(con, tabel, kolom):
    try:
        ada = {r[1] for r in con.execute("PRAGMA table_info(%s)" % tabel)}
    except sqlite3.Error:
        return False
    return set(kolom) <= ada


# --------------------------------------------------------------------------- bagian: penjualan (kasir)
def rentang_hari(dari, sampai):
    d = dari
    while d <= sampai:
        yield d
        d += timedelta(days=1)


def ambil_kasir(ctx):
    k = ctx["alat"]["kasir"]
    script, db, per = k["script_path"], k["snap"], ctx["periode"]

    def rekap(dari, sampai):
        if dari == sampai:
            a = ["rekap", "--db", str(db), "--tanggal", dari.isoformat(), "--json"]
        else:
            a = ["rekap", "--db", str(db), "--dari", dari.isoformat(), "--sampai", sampai.isoformat(), "--json"]
        return jalankan(script, a, ctx["timeout"])

    info = jalankan(script, ["info", "--db", str(db), "--json"], ctx["timeout"])
    kini = rekap(per["dari"], per["sampai"])
    hasil = {"sumber": "kasir-lokal", "omzet": int(kini.get("penjualan_bersih", 0)),
             "uang_diterima": int(kini.get("total_diterima", 0)), "ppn": int(kini.get("ppn", 0)),
             "nota": int(kini.get("nota_jual", 0)), "nota_retur": int(kini.get("nota_retur", 0)),
             "nota_void": int(kini.get("nota_void", 0)), "retur_void_rp": int(kini.get("retur_void", 0)),
             "diskon": int(kini.get("diskon", 0)),

             "per_metode": {m: int(v) for m, v in (kini.get("per_metode") or {}).items()},
             "terlaris": [{"kode": p.get("kode"), "nama": p.get("nama"), "qty": p.get("qty"), "netto": int(p.get("netto", 0))}
                          for p in (kini.get("per_produk") or []) if int(p.get("netto", 0)) > 0][:ctx["maks_produk"]],
             "per_hari": kini.get("per_hari") or {}, "banding": {}}
    # Rata-rata per nota = omzet bersih / (nota jual - nota void), dibulatkan ke rupiah terdekat (0,5 ke atas).
    hasil["nota_sah"] = max(hasil["nota"] - hasil["nota_void"], 0)
    hasil["rata_rata_per_nota"] = (int((Decimal(hasil["omzet"]) / hasil["nota_sah"]).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
                                   if hasil["nota_sah"] else None)
    for nama, dari, sampai in per["banding"]:
        try:
            b = rekap(dari, sampai)
            om, nt = int(b.get("penjualan_bersih", 0)), int(b.get("nota_jual", 0))
        except GagalAlat:
            om = nt = None
        pr, teks = persen(hasil["omzet"], om)
        hasil["banding"][nama] = {"dari": dari.isoformat(), "sampai": sampai.isoformat(), "omzet": om, "nota": nt,
                                  "selisih": (hasil["omzet"] - om) if om is not None else None,
                                  "persen": pr, "teks": teks}
    hasil["pengaturan_stok"] = (info.get("pengaturan") or {}).get("stok")
    hasil["zona_toko"] = (info.get("pengaturan") or {}).get("zona")
    hasil["sesi_terbuka"] = None
    st = info.get("sesi_terbuka")
    if st:
        hasil["sesi_terbuka"] = {"buka": st.get("buka"), "kas_awal": st.get("kas_awal")}
    # Selisih kas: tidak ada di perintah resmi -> baca tabel sesi di snapshot bila kolomnya ada.
    hasil["tutup_kasir"] = []
    con = sqlite3.connect(str(db))
    try:
        if kolom_ada(con, "sesi", ["tutup", "kas_seharusnya", "kas_fisik", "selisih"]):
            for r in con.execute("SELECT tutup, kas_seharusnya, kas_fisik, selisih FROM sesi WHERE tutup IS NOT NULL "
                                 "AND substr(tutup,1,10) BETWEEN ? AND ? ORDER BY tutup",
                                 (per["dari"].isoformat(), per["sampai"].isoformat())):
                hasil["tutup_kasir"].append({"tutup": r[0], "kas_seharusnya": r[1], "kas_fisik": r[2], "selisih": r[3]})
        else:
            ctx["catatan"].append("Selisih kas tidak dibaca: struktur tabel sesi kasir berubah.")
    finally:
        con.close()
    return hasil


def ambil_penjualan_dari_stok(ctx):
    """Tanpa kasir: omzet tercatat di buku-stok (laporan ringkas per hari, dijumlahkan)."""
    k = ctx["alat"]["stok"]
    per = ctx["periode"]

    def total(dari, sampai):
        om = qty = 0
        for d in rentang_hari(dari, sampai):
            r = jalankan(k["script_path"], ["laporan", "ringkas", "--db", str(k["snap"]), "--tanggal", d.isoformat(),
                                            "--json"], ctx["timeout"])
            om += int(r.get("omzet_tercatat", 0))
            qty += Decimal(str(r.get("terjual_qty", 0)))
        return om, qty

    om, qty = total(per["dari"], per["sampai"])
    hasil = {"sumber": "buku-stok", "omzet": om, "terjual_qty": str(qty), "banding": {}}
    for nama, dari, sampai in per["banding"]:
        try:
            b, _ = total(dari, sampai)
        except GagalAlat:
            b = None
        pr, teks = persen(om, b)
        hasil["banding"][nama] = {"dari": dari.isoformat(), "sampai": sampai.isoformat(), "omzet": b,
                                  "selisih": (om - b) if b is not None else None, "persen": pr, "teks": teks}
    return hasil


# --------------------------------------------------------------------------- bagian: stok
def ambil_stok(ctx):
    k = ctx["alat"]["stok"]
    per = ctx["periode"]
    r = jalankan(k["script_path"], ["laporan", "ringkas", "--db", str(k["snap"]), "--tanggal",
                                    per["sampai"].isoformat(), "--json"], ctx["timeout"])
    daftar = r.get("stok_menipis") or []
    hasil = {"posisi_per": ctx["dibuat"], "minus": [], "habis": [], "menipis": [],
             "pesanan_belum_dikemas": int(r.get("pesanan_belum_dikemas", 0)),
             "nilai_persediaan": r.get("nilai_persediaan"),
             "tidak_laku": r.get("tidak_laku")}
    for p in daftar:
        item = {"sku": p.get("sku"), "nama": p.get("nama"), "stok": p.get("stok"), "stok_min": p.get("stok_min"),
                "kurang_dari_minimum": p.get("kurang_dari_minimum"),
                "perkiraan_habis_hari": p.get("perkiraan_habis_hari"), "status": p.get("status")}
        st = str(p.get("status", "")).upper()
        (hasil["minus"] if st == "MINUS" else hasil["habis"] if st == "HABIS" else hasil["menipis"]).append(item)
    return hasil


def cek_impor_kasir_ke_stok(ctx, kasir):
    """Bila kasir diatur 'stok dikelola buku-stok', tiap nota jual kasir yang SAH (bukan yang di-void) pada hari
    itu harus punya baris di tabel `pesanan` buku-stok (no_pesanan = nomor nota kasir, mis. N-260924-0001; lihat
    kasir.py cmd_ekspor & stok.py cmd_impor_pesanan). Nota yang di-void sengaja TIDAK pernah masuk ke `pesanan`
    (statusnya "Dibatalkan" -> kategori "batal" -> stok.py tidak membuat baris sama sekali), jadi nota itu tidak
    dihitung sebagai "belum diimpor". Membandingkan per nomor nota (bukan sekadar "ada >=1 nota"), supaya impor
    SEBAGIAN (sebagian nota sudah, sebagian belum) tetap terdeteksi.

    Mengembalikan list [{"tanggal","kurang","total"}, ...] untuk hari yang punya nota belum diimpor, atau None
    bila cek dilewati (struktur tabel berubah / alat tidak lengkap)."""
    if kasir.get("pengaturan_stok") != "buku-stok" or ctx["alat"]["stok"]["status"] != "ada":
        return None
    hari_ada = [h for h, v in (kasir.get("per_hari") or {}).items() if v]
    if not hari_ada:
        return None
    con_k = sqlite3.connect(str(ctx["alat"]["kasir"]["snap"]))
    try:
        if not kolom_ada(con_k, "nota", ["id", "no", "jenis", "waktu", "ref_nota_id"]):
            ctx["catatan"].append("Cek impor kasir ke buku-stok dilewati: struktur tabel nota kasir berubah.")
            return None
        nota_per_hari = {}
        for h in hari_ada:
            baris = con_k.execute(
                "SELECT no FROM nota WHERE jenis='jual' AND substr(waktu,1,10)=? AND id NOT IN "
                "(SELECT ref_nota_id FROM nota WHERE jenis='void' AND ref_nota_id IS NOT NULL)", (h,)).fetchall()
            nota_per_hari[h] = [r[0] for r in baris]
    finally:
        con_k.close()
    con_s = sqlite3.connect(str(ctx["alat"]["stok"]["snap"]))
    try:
        if not kolom_ada(con_s, "pesanan", ["no_pesanan"]):
            ctx["catatan"].append("Cek impor kasir ke buku-stok dilewati: struktur tabel pesanan berubah.")
            return None
        belum = []
        for h in sorted(hari_ada):
            nomor = nota_per_hari.get(h) or []
            if not nomor:
                continue
            ada = 0
            for no in nomor:
                if con_s.execute("SELECT 1 FROM pesanan WHERE no_pesanan=?", (no,)).fetchone():
                    ada += 1
            kurang = len(nomor) - ada
            if kurang:
                belum.append({"tanggal": h, "kurang": kurang, "total": len(nomor)})
        return belum
    finally:
        con_s.close()


def jadwal_masuk_paling_awal(ctx):
    """Jam masuk paling awal di antara shift yang dipakai karyawan aktif (absensi-lokal), format 'HH:MM'.

    Dipakai untuk menghindari alarm palsu "belum ada data absen" sebelum toko/karyawan mulai kerja (bukan
    perhitungan jadwal per-hari yang persis; hanya jam mulai paling awal yang ada di data shift). None bila
    tidak terbaca (struktur tabel berubah, atau tidak ada karyawan/shift)."""
    a = ctx["alat"]["absensi"]
    if a.get("status") != "ada":
        return None
    con = sqlite3.connect(str(a["snap"]))
    try:
        if not kolom_ada(con, "karyawan", ["shift", "aktif"]) or not kolom_ada(con, "shift", ["kode", "masuk"]):
            return None
        r = con.execute("SELECT MIN(s.masuk) FROM shift s JOIN karyawan k ON k.shift = s.kode "
                        "WHERE k.aktif = 1").fetchone()
        nilai = r[0] if r else None
        return nilai if nilai and re.fullmatch(r"\d{2}:\d{2}", nilai) else None
    except sqlite3.Error:
        return None
    finally:
        con.close()


# --------------------------------------------------------------------------- bagian: kehadiran
POLA_TELAT = re.compile(r"^(.*) (\d{1,2}\.\d{2}) \((\d+) menit\)$")
POLA_KET = re.compile(r"^(.*) \(([^()]+)\)$")
POLA_LEMBUR = re.compile(r"^(.*) ([\d.,]+) jam$")


def ambil_absensi(ctx):
    k = ctx["alat"]["absensi"]
    per = ctx["periode"]
    sam = ctx["samarkan"]

    def nm(n):
        return inisial(n) if sam else n

    if per["jenis"] == "harian":
        a = ["harian", "--db", str(k["snap"]), "--tanggal", per["dari"].isoformat(), "--json"]
        kini = ctx["sekarang_lokal"]
        try:
            r = jalankan(k["script_path"], a + ["--sekarang", kini], ctx["timeout"])
        except GagalAlat as e:
            if "versi alat tidak cocok" not in str(e):
                raise
            r = jalankan(k["script_path"], a, ctx["timeout"])  # alat versi lain tanpa --sekarang
        hasil = {"jenis": "harian", "terjadwal": int(r.get("terjadwal", 0)), "hadir": [], "terlambat": [],
                 "pulang_cepat": [], "izin_sakit_cuti_dinas": [], "alpa": [], "tanpa_keterangan": [],
                 "masuk_hari_libur": [], "lembur_disetujui": [], "lembur_perlu_keputusan": [], "perlu_dicek": []}
        hasil["hadir"] = [nm(n) for n in r.get("hadir") or []]
        for s in r.get("terlambat") or []:
            m = POLA_TELAT.match(s)
            hasil["terlambat"].append({"nama": nm(m.group(1)), "jam": m.group(2), "menit": int(m.group(3))} if m
                                      else {"nama": None if sam else s, "jam": None, "menit": None})
        for s in r.get("pulang_cepat") or []:
            m = POLA_TELAT.match(s)
            hasil["pulang_cepat"].append({"nama": nm(m.group(1)), "jam": m.group(2), "menit": int(m.group(3))} if m
                                         else {"nama": None if sam else s, "jam": None, "menit": None})
        for s in r.get("keterangan") or []:
            m = POLA_KET.match(s)
            nama, jenis = (m.group(1), m.group(2).strip().lower()) if m else (s, "keterangan")
            if jenis == "alpa":
                hasil["alpa"].append(nm(nama))
            else:
                hasil["izin_sakit_cuti_dinas"].append({"nama": nm(nama), "jenis": jenis})
        hasil["tanpa_keterangan"] = [nm(n) for n in r.get("belum_absen") or []]
        hasil["masuk_hari_libur"] = [nm(n) for n in r.get("masuk_hari_libur") or []]
        for s in r.get("lembur") or []:
            m = POLA_LEMBUR.match(s)
            hasil["lembur_disetujui"].append({"nama": nm(m.group(1)), "jam": m.group(2)} if m
                                             else {"nama": None if sam else s, "jam": None})
        hasil["hari_ini"] = per["dari"] == ctx["hari_ini"]
    else:
        a = ["rekap", "--db", str(k["snap"]), "--dari", per["dari"].isoformat(), "--sampai",
             per["sampai"].isoformat(), "--json"]
        r = jalankan(k["script_path"], a, ctx["timeout"])
        hasil = {"jenis": "mingguan", "karyawan": 0, "hari_terjadwal": 0, "hari_hadir": 0, "terlambat_kali": 0,
                 "terlambat_menit": 0, "izin": 0, "sakit": 0, "cuti": 0, "dinas": 0, "alpa": 0, "tanpa_keterangan": 0,
                 "lembur_jam": "0", "sering_terlambat": [], "lembur_perlu_keputusan": [], "perlu_dicek": [],
                 "ada_data_absen": bool(r.get("ada_data_absen", True))}
        lembur = Decimal(0)
        for kr in r.get("karyawan") or []:
            hasil["karyawan"] += 1
            hasil["hari_terjadwal"] += int(kr.get("hari_terjadwal", 0))
            hasil["hari_hadir"] += int(kr.get("hadir", 0)) + int(kr.get("hadir_di_hari_libur", 0))
            for f in ("terlambat_kali", "terlambat_menit", "izin", "sakit", "cuti", "dinas", "alpa", "tanpa_keterangan"):
                hasil[f] += int(kr.get(f, 0) or 0)
            for f in ("lembur_jam_hari_kerja", "lembur_jam_hari_libur"):
                try:
                    lembur += Decimal(str(kr.get(f) or "0"))
                except Exception:
                    pass
            if int(kr.get("terlambat_kali", 0) or 0) > 0:
                hasil["sering_terlambat"].append({"nama": nm(kr.get("nama")), "kali": int(kr["terlambat_kali"]),
                                                  "menit": int(kr.get("terlambat_menit", 0) or 0)})
        hasil["sering_terlambat"].sort(key=lambda x: (-x["kali"], -x["menit"]))
        hasil["sering_terlambat"] = hasil["sering_terlambat"][:5]
        hasil["lembur_jam"] = fq(lembur)
    for m in r.get("masalah") or []:
        jenis, nama = m.get("jenis"), m.get("nama") or ""
        if jenis in ("pulang_lewat_jadwal", "masuk_libur_tanpa_lembur"):
            hasil["lembur_perlu_keputusan"].append({"nama": nm(nama), "tanggal": m.get("tanggal") or "",
                                                     "jenis": jenis, "pesan": m.get("pesan", "")})
        elif m.get("tingkat") in ("salah", "cek"):
            hasil["perlu_dicek"].append({"nama": nm(nama), "tanggal": m.get("tanggal") or "", "jenis": jenis,
                                         "pesan": m.get("pesan", "")})
    return hasil


# --------------------------------------------------------------------------- bagian: tagihan
def ambil_pengingat(ctx):
    k = ctx["alat"]["pengingat"]
    r = jalankan(k["script_path"], ["--file", str(k["snap"]), "--hari-ini", ctx["hari_ini"].isoformat(),
                                    "--tz", ctx["tz_nama"], "rekap"], ctx["timeout"])

    def ringkas(it, ket):
        # Sengaja TANPA nama pelanggan/perihal: hanya nomor item, jenis, nominal, dan waktu.
        return {"id": str(it.get("id")), "jenis": it.get("jenis"), "nominal": it.get("nominal"), "keterangan": ket}

    terlambat = [ringkas(i, "lewat %s hari" % i.get("hari_terlambat", "?")) for i in r.get("terlambat") or []]
    hari_ini = [ringkas(i, "hari ini") for i in r.get("jatuh_tempo_hari_ini") or []]
    besok = [ringkas(i, "besok") for i in r.get("besok_h_1") or []]
    ring = r.get("ringkasan") or {}
    return {"hari_acuan": ctx["hari_ini"].isoformat(), "jumlah_aktif": int(r.get("jumlah_aktif", 0)),
            "terlambat": terlambat, "hari_ini": hari_ini, "besok": besok,
            "tujuh_hari_ke_depan": len(r.get("tujuh_hari_ke_depan") or []),
            "piutang_terlambat": int(ring.get("piutang_terlambat", 0) or 0),
            "piutang_hari_ini": int(ring.get("piutang_hari_ini", 0) or 0),
            "total_tertunggak": int(ring.get("total_tertunggak", 0) or 0),
            "baris_ditolak": len(r.get("baris_ditolak") or [])}


# --------------------------------------------------------------------------- bagian: prospek (crm-wa)
def ambil_crm(ctx):
    """PROSPEK dari crm-wa. Semua angka dipakai APA ADANYA dari `crm.py rekap --json` (kontrak `skema_json` 1;
    tanpa nama/nomor prospek) -- tidak dihitung ulang dengan rumus lain. `--dari`/`--sampai` mengikuti periode
    laporan (lead masuk & deal periode itu); `--hari-ini` selalu hari acuan laporan (bukan periode), supaya
    status follow-up (terlambat/hari ini) menggambarkan kondisi pipeline SAAT INI, sama seperti bagian TAGIHAN
    & FOLLOW-UP (pengingat-follow-up) yang juga tidak terikat periode yang sedang dilaporkan."""
    k = ctx["alat"]["crm"]
    per = ctx["periode"]

    def rekap(dari, sampai):
        return jalankan(k["script_path"], ["rekap", "--db", str(k["snap"]), "--dari", dari.isoformat(), "--sampai",
                                           sampai.isoformat(), "--hari-ini", ctx["hari_ini"].isoformat(), "--json"],
                        ctx["timeout"])

    kini = rekap(per["dari"], per["sampai"])
    pi = kini.get("periode_ini") or {}
    db_ = pi.get("deal_baru") or {}
    ko = pi.get("kohort") or {}
    f = kini.get("followup") or {}
    tb = kini.get("sumber_terbaik")
    hasil = {"sumber": "crm-wa", "lead_masuk": int(pi.get("lead_masuk", 0)),
             "deal": {"jumlah": int(db_.get("jumlah", 0)), "nilai": int(db_.get("nilai", 0)),
                      "tanpa_nilai": int(db_.get("tanpa_nilai", 0))},
             "konversi_persen": pi.get("konversi_persen"), "konversi_teks": pi.get("konversi_teks", "-"),
             "kohort": {"lead": int(ko.get("lead", 0)), "deal_atau_selesai": int(ko.get("deal_atau_selesai", 0)),
                        "batal": int(ko.get("batal", 0)), "masih_berjalan": int(ko.get("masih_berjalan", 0))},
             "followup": {"terlambat": int(f.get("terlambat", 0)), "hari_ini": int(f.get("hari_ini", 0)),
                          "besok": int(f.get("besok", 0)),
                          "order_perlu_konfirmasi": int(f.get("order_perlu_konfirmasi", 0)),
                          "nilai_terlambat_dan_hari_ini": int(f.get("nilai_terlambat_dan_hari_ini", 0))},
             "sumber_terbaik": ({"sumber": tb.get("sumber"), "lead": int(tb.get("lead", 0)),
                                 "deal": int(tb.get("deal", 0)), "konversi_teks": tb.get("konversi_teks", "-"),
                                 "sampel_kecil": bool(tb.get("sampel_kecil"))} if tb else None),
             "banding": {}}
    if per["jenis"] == "mingguan":
        for nama, dari, sampai in per["banding"]:
            try:
                lead_b = int((rekap(dari, sampai).get("periode_ini") or {}).get("lead_masuk", 0))
            except GagalAlat:
                lead_b = None
            pr, teks = persen(hasil["lead_masuk"], lead_b, satuan="0") if lead_b is not None else \
                (None, "tidak ada data pembanding")
            hasil["banding"][nama] = {"dari": dari.isoformat(), "sampai": sampai.isoformat(), "lead_masuk": lead_b,
                                      "persen_lead": pr, "teks_lead": teks}
    return hasil


# --------------------------------------------------------------------------- susun
def siapkan_alat(args, tmp):
    alat = {}
    for nama in ALAT:
        a = {"skill": ALAT[nama]["skill"], "status": "tidak_ada", "pesan": ""}
        if nama in args.tanpa:
            a.update(status="dilewati", pesan="dilewati atas permintaan (--tanpa)")
            alat[nama] = a
            continue
        if nama == "pengingat":
            if args.pengingat:
                src = Path(args.pengingat).expanduser()
                ada = src.is_file()
            else:
                src = next((p for p in kandidat_pengingat() if p.is_file()), None)
                ada = src is not None
        else:
            src = Path(getattr(args, nama + "_db")).expanduser() if getattr(args, nama + "_db") else path_db_default(nama)
            ada = src.is_file()
        a["data"] = str(src) if src else None
        if not ada:
            a["pesan"] = ("file data tidak ditemukan di %s" % src) if src else "file pengingat/DAFTAR.csv tidak ditemukan"
            alat[nama] = a
            continue
        script = cari_script(nama, getattr(args, nama + "_script"))
        if not script:
            a.update(status="gagal", pesan="data ada, tetapi script %s tidak ditemukan. Pasang skill %s di folder skills "
                     "yang sama, atau beri --%s-script PATH." % (ALAT[nama]["script"], ALAT[nama]["skill"], nama))
            alat[nama] = a
            continue
        a["script"] = str(script)
        a["script_path"] = script
        snap = Path(tmp) / (nama + (".csv" if nama == "pengingat" else ".db"))
        try:
            if nama == "pengingat":
                shutil.copyfile(str(src), str(snap))
            else:
                snapshot(src, snap, args.timeout)
        except (GagalAlat, OSError) as e:
            a.update(status="gagal", pesan=str(e))
            alat[nama] = a
            continue
        a["snap"] = snap
        a["status"] = "ada"
        alat[nama] = a
    return alat


def bagian(ctx, nama, fungsi):
    try:
        return fungsi(ctx)
    except GagalAlat as e:
        a = ctx["alat"][nama]
        pesan = str(e)
        snap, asli = a.get("snap"), a.get("data")
        if snap and asli:
            # Pesan dari alat (mis. "no such table: meta") bisa memuat path SALINAN sementara (--db yang
            # kita berikan ke alat), bukan file asli. Ganti agar pengguna tidak bingung/mencari file yang salah.
            pesan = pesan.replace(str(snap), asli)
        a["status"] = "gagal"
        a["pesan"] = pesan
        return None


def susun(args):
    tz, label_tz, tz_nama = zona(args.tz)
    now = waktu_sekarang(args, tz)
    hari_ini = now.date()
    per = tentukan_periode(args, hari_ini)
    ctx = {"periode": per, "hari_ini": hari_ini, "tz_nama": tz_nama, "timeout": args.timeout,
           "samarkan": args.samarkan, "maks_produk": args.maks_produk, "catatan": [], "jadwal_awal": None,
           "dibuat": now.strftime("%Y-%m-%d %H:%M") + " " + label_tz,
           "sekarang_lokal": now.strftime("%Y-%m-%d %H:%M")}
    tmp = tempfile.mkdtemp(prefix="laporan-usaha-")
    try:
        ctx["alat"] = siapkan_alat(args, tmp)
        A = ctx["alat"]
        penjualan = stok = hadir = tagihan = prospek = None
        if A["kasir"]["status"] == "ada":
            penjualan = bagian(ctx, "kasir", ambil_kasir)
        if penjualan is None and A["kasir"]["status"] == "tidak_ada" and A["stok"]["status"] == "ada":
            penjualan = bagian(ctx, "stok", ambil_penjualan_dari_stok)
        if A["stok"]["status"] == "ada":
            stok = bagian(ctx, "stok", ambil_stok)
        if A["absensi"]["status"] == "ada":
            hadir = bagian(ctx, "absensi", ambil_absensi)
            ctx["jadwal_awal"] = jadwal_masuk_paling_awal(ctx)
        if A["pengingat"]["status"] == "ada":
            tagihan = bagian(ctx, "pengingat", ambil_pengingat)
        if A["crm"]["status"] == "ada":
            prospek = bagian(ctx, "crm", ambil_crm)
        belum_impor = None
        if penjualan and penjualan.get("sumber") == "kasir-lokal" and stok is not None:
            belum_impor = cek_impor_kasir_ke_stok(ctx, penjualan)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    perhatian = susun_perhatian(ctx, penjualan, stok, hadir, tagihan, prospek, belum_impor)
    alat_publik = {n: {k: v for k, v in a.items() if k in ("skill", "status", "pesan", "data", "script")}
                   for n, a in ctx["alat"].items()}
    data = {"ok": True, "versi": VERSI,
            "periode": {"jenis": per["jenis"], "dari": per["dari"].isoformat(), "sampai": per["sampai"].isoformat(),
                        "minggu_berjalan": bool(per.get("berjalan")), "zona_waktu": tz_nama, "dibuat": ctx["dibuat"],
                        "pembanding": [{"nama": n, "dari": d.isoformat(), "sampai": s.isoformat()} for n, d, s in per["banding"]]},
            "alat": alat_publik, "penjualan": penjualan, "stok": stok, "kehadiran": hadir, "tagihan": tagihan,
            "prospek": prospek, "perhatian": perhatian, "catatan": ctx["catatan"],
            "rumus": {"perubahan_persen": "(nilai periode ini - nilai pembanding) / nilai pembanding x 100, dibulatkan 1 "
                                          "desimal (0,05 ke atas). Pembanding Rp 0 atau minus: persen tidak dihitung.",
                      "omzet": "penjualan bersih kasir-lokal = setelah diskon, retur & void (angka dari kasir-lokal).",
                      "rata_rata_per_nota": "omzet bersih / (nota jual - nota void), dibulatkan ke rupiah terdekat (0,5 ke atas).",
                      "prospek": "Semua angka PROSPEK diambil apa adanya dari crm.py rekap --json (skema_json 1); "
                                 "tidak dihitung ulang. Follow-up terlambat/hari ini selalu dihitung per hari ini "
                                 "(bukan per periode laporan), sama seperti TAGIHAN & FOLLOW-UP."}}
    data["teks"] = teks_laporan(data, per, ctx)
    return data


def susun_perhatian(ctx, pj, stok, hd, tg, pr, belum_impor):
    p = []
    lokal = datetime.now().astimezone().utcoffset()
    target = datetime.now(timezone.utc).astimezone(zona(ctx["tz_nama"])[0]).utcoffset()
    if ctx["alat"]["absensi"]["status"] == "ada" and lokal != target:
        p.append("Jam komputer ini bukan %s (selisih %s jam). absensi-lokal mencatat jam tap menurut jam komputer, "
                 "jadi tap dekat tengah malam bisa masuk ke tanggal lain. Samakan zona waktu komputer."
                 % (ctx["tz_nama"], fq(Decimal((target - lokal).total_seconds()) / 3600)))
    if pj and pj.get("sumber") == "kasir-lokal" and pj.get("zona_toko"):
        toko = TZ_TETAP.get(pj["zona_toko"].lower())
        lapor = TZ_TETAP.get(ctx["tz_nama"].lower())
        if toko and lapor and toko[0] != lapor[0]:
            p.append("Toko diatur zona %s (%s) tapi laporan memakai --tz %s (%s). kasir-lokal mencatat nota "
                      "menurut zona toko (bukan jam komputer); pakai --tz %s agar tanggal penjualan cocok."
                      % (pj["zona_toko"], toko[1], ctx["tz_nama"], lapor[1], pj["zona_toko"]))
    if pj and pj.get("sumber") == "kasir-lokal":
        for t in pj.get("tutup_kasir") or []:
            s = t.get("selisih")
            if s:
                p.append("Selisih kas saat tutup kasir %s: %s %s (seharusnya %s, dihitung %s)." % (
                    str(t.get("tutup"))[:16], "LEBIH" if s > 0 else "KURANG", rp(abs(s)), rp(t.get("kas_seharusnya") or 0),
                    rp(t.get("kas_fisik") or 0)))
        buka = str((pj.get("sesi_terbuka") or {}).get("buka") or "")
        if buka and ctx["periode"]["jenis"] == "harian" and buka[:10] <= ctx["periode"]["sampai"].isoformat():
            p.append("Kasir belum ditutup (dibuka %s). Tutup kasir agar uang laci dicocokkan." %
                     str(pj["sesi_terbuka"].get("buka"))[:16])
        if pj.get("nota_void") or pj.get("nota_retur"):
            p.append("Ada %d void & %d retur (%s). Cek alasannya di kasir." % (
                pj.get("nota_void", 0), pj.get("nota_retur", 0), rp(abs(pj.get("retur_void_rp", 0)))))
    if belum_impor:
        total_kurang = sum(b["kurang"] for b in belum_impor)
        total_semua = sum(b["total"] for b in belum_impor)
        tanggal_str = ", ".join(b["tanggal"] for b in belum_impor)
        p.append("%d dari %d nota kasir tanggal %s belum diimpor ke buku-stok (stok belum terpotong)."
                 % (total_kurang, total_semua, tanggal_str))
    if stok:
        if stok["minus"]:
            p.append("Stok MINUS %d barang (%s). Lakukan stock opname." % (
                len(stok["minus"]), ", ".join(str(x["sku"]) for x in stok["minus"][:5])))
        if stok["pesanan_belum_dikemas"]:
            p.append("%d pesanan marketplace belum dikemas." % stok["pesanan_belum_dikemas"])
    if hd:
        if hd["jenis"] == "harian":
            kosong = (hd["terjadwal"] and not hd["hadir"] and not hd["izin_sakit_cuti_dinas"] and not hd["alpa"]
                      and len(hd["tanpa_keterangan"]) >= hd["terjadwal"])
            awal = ctx.get("jadwal_awal")
            belum_waktunya = (kosong and hd.get("hari_ini") and awal
                               and ctx["sekarang_lokal"][-5:] < awal)
            if belum_waktunya:
                p.append("Belum waktunya absen (jadwal mulai %s)." % awal.replace(":", "."))
            elif kosong:
                p.append("Belum ada satu pun data absen hari itu. File mesin absen mungkin belum diimpor.")
            elif hd["tanpa_keterangan"]:
                label = "Belum absen tanpa keterangan" if hd.get("hari_ini") else "Tidak absen & tanpa keterangan"
                p.append("%s (%d): %s. Tanyakan & catat izin/alpa." % (
                    label, len(hd["tanpa_keterangan"]), ", ".join(hd["tanpa_keterangan"])))
        elif not hd.get("ada_data_absen", True):
            p.append("Tidak ada data absen minggu itu. File mesin absen mungkin belum diimpor.")
        elif hd.get("tanpa_keterangan"):
            p.append("%d hari kerja karyawan tanpa absen & tanpa keterangan. Tanyakan & catat izin/alpa."
                     % hd["tanpa_keterangan"])
        if hd["lembur_perlu_keputusan"]:
            p.append("%d kejadian pulang lewat jadwal/masuk hari libur tanpa lembur disetujui. Putuskan: catat lembur "
                     "atau abaikan." % len(hd["lembur_perlu_keputusan"]))
        if hd["perlu_dicek"]:
            p.append("%d data absen ganjil perlu dicek (mis. tap tidak lengkap)." % len(hd["perlu_dicek"]))
    if tg:
        if tg["terlambat"]:
            p.append("%d tagihan/follow-up terlambat%s." % (
                len(tg["terlambat"]), (", piutang " + rp(tg["piutang_terlambat"])) if tg["piutang_terlambat"] else ""))
        if tg["baris_ditolak"]:
            p.append("%d baris di daftar pengingat rusak & dilewati. Ketik 'rekap pengingat' untuk rinciannya."
                     % tg["baris_ditolak"])
    if pr and pr["followup"]["terlambat"]:
        p.append("%d follow-up prospek CRM terlambat. Ketik 'follow-up hari ini' untuk daftar & draf pesannya."
                 % pr["followup"]["terlambat"])
    if not any(a["status"] in ("ada", "gagal") for a in ctx["alat"].values()):
        p.append("Belum ada data dari alat mana pun (kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up, "
                 "crm-wa). Jika alatnya sudah dipakai di lokasi lain, beri tahu lokasinya (opsi --kasir-db, "
                 "--stok-db, --absensi-db, --pengingat, --crm-db).")
    for n, a in ctx["alat"].items():
        if a["status"] == "gagal":
            p.append("%s tidak terbaca: %s" % (a["skill"], a["pesan"]))
    return p


def teks_laporan(data, per, ctx):
    A = ctx["alat"]
    t = []
    if per["jenis"] == "harian":
        t += ["LAPORAN HARIAN USAHA", tgl_id(per["dari"])]
    else:
        t += ["LAPORAN MINGGUAN USAHA", "%s - %s%s" % (tgl_id(per["dari"], False), tgl_id(per["sampai"], False),
                                                      " (minggu berjalan, s.d. hari ini)" if per.get("berjalan") else "")]
    t.append("Dibuat %s" % data["periode"]["dibuat"])

    # Penjualan
    pj = data["penjualan"]
    t += ["", "PENJUALAN" + (" (dari buku-stok)" if pj and pj.get("sumber") == "buku-stok" else "")]
    if not pj:
        t.append(pesan_kosong(A, "kasir"))
    else:
        if pj["sumber"] == "kasir-lokal":
            if not pj["nota"] and not pj["nota_retur"] and not pj["nota_void"]:
                t.append("Belum ada transaksi tercatat di kasir.")
            else:
                t.append("Omzet bersih: %s" % rp(pj["omzet"]))
                if pj["uang_diterima"] != pj["omzet"]:
                    t.append("Uang diterima: %s (selisih %s = pajak/service yang dicatat kasir)"
                             % (rp(pj["uang_diterima"]), rp(pj["uang_diterima"] - pj["omzet"])))
                t.append("Nota: %d%s | rata-rata %s" % (
                    pj["nota_sah"], (" (+%d dibatalkan)" % pj["nota_void"]) if pj["nota_void"] else "",
                    rp(pj["rata_rata_per_nota"]) if pj["rata_rata_per_nota"] is not None else "-"))
        else:
            t.append("Omzet tercatat: %s (%s barang)" % (rp(pj["omzet"]), fq(pj["terjual_qty"])))
        for nama, dari, sampai in per["banding"]:
            b = pj["banding"][nama]
            label = {"kemarin": "vs kemarin (%s)" % tgl_pendek(dari),
                     "minggu_lalu": "vs %s lalu (%d/%d)" % (HARI[dari.weekday()], dari.day, dari.month),
                     "minggu_sebelumnya": "vs %d/%d-%d/%d" % (dari.day, dari.month, sampai.day, sampai.month)}[nama]
            if b["omzet"] is None:
                t.append("%s: tidak ada data pembanding" % label)
            else:
                t.append("%s: %s -> %s" % (label, rp(b["omzet"]), b["teks"]))
        if pj["sumber"] == "kasir-lokal" and pj["per_metode"]:
            beda_pajak = pj["uang_diterima"] != pj["omzet"]
            t.append("Per metode bayar%s:" % (" (termasuk pajak/service, omzet di atas belum termasuk)" if beda_pajak else ""))
            for m, v in sorted(pj["per_metode"].items(), key=lambda x: -x[1]):
                t.append("- %s %s" % (m, rp(v)))
        if pj["sumber"] == "kasir-lokal" and pj["terlaris"]:
            t.append("Terlaris:")
            for i, p in enumerate(pj["terlaris"], 1):
                t.append("%d. %s: %s terjual, %s" % (i, p["nama"], fq(p["qty"]), rp(p["netto"])))
        if pj["sumber"] == "kasir-lokal" and (pj["nota_retur"] or pj["nota_void"]):
            t.append("Retur %d | void %d (%s)" % (pj["nota_retur"], pj["nota_void"], rp(abs(pj["retur_void_rp"]))))

    # Stok
    st = data["stok"]
    t += ["", "STOK"]
    if not st:
        t.append(pesan_kosong(A, "stok"))
    else:
        t.append("Posisi per %s" % st["posisi_per"])
        if not (st["minus"] or st["habis"] or st["menipis"]):
            t.append("Semua stok di atas batas minimum.")
        else:
            t.append("Minus %d | habis %d | menipis %d" % (len(st["minus"]), len(st["habis"]), len(st["menipis"])))
            semua = st["minus"] + st["habis"] + st["menipis"]
            for p in semua[:8]:
                extra = ""
                if p.get("perkiraan_habis_hari") is not None and p["status"] == "MENIPIS":
                    extra = ", habis +-%s hari" % p["perkiraan_habis_hari"]
                t.append("- %s %s: stok %s (min %s) %s%s" % (p["sku"], p["nama"], fq(p["stok"]), fq(p["stok_min"]),
                                                             p["status"], extra))
            if len(semua) > 8:
                t.append("... dan %d barang lain (ketik 'stok menipis')" % (len(semua) - 8))
            restock = [p for p in semua if p.get("kurang_dari_minimum")]
            if restock:
                t.append("Perlu restock (sampai batas minimum): " + ", ".join(
                    "%s %s" % (p["sku"], fq(p["kurang_dari_minimum"])) for p in restock[:8]))
        t.append("Pesanan belum dikemas: %d" % st["pesanan_belum_dikemas"])

    # Kehadiran
    hd = data["kehadiran"]
    t += ["", "KEHADIRAN"]
    if not hd:
        t.append(pesan_kosong(A, "absensi"))
    elif hd["jenis"] == "harian":
        t.append("Hadir %d dari %d terjadwal" % (len(hd["hadir"]), hd["terjadwal"]))
        if hd["terlambat"]:
            t.append("Terlambat (%d): %s" % (len(hd["terlambat"]), ", ".join(
                ("%s %s (%d mnt)" % (x["nama"], x["jam"], x["menit"])) if x["jam"] else (x["nama"] or "1 orang")
                for x in hd["terlambat"])))
        if hd["izin_sakit_cuti_dinas"]:
            t.append("Izin/sakit/cuti/dinas (%d): %s" % (len(hd["izin_sakit_cuti_dinas"]), ", ".join(
                "%s (%s)" % (x["nama"], x["jenis"]) for x in hd["izin_sakit_cuti_dinas"])))
        t.append("Alpa: %s" % (("%d (%s)" % (len(hd["alpa"]), ", ".join(hd["alpa"]))) if hd["alpa"] else "0"))
        if hd["tanpa_keterangan"]:
            t.append("%s (%d): %s" % ("Belum absen" if hd.get("hari_ini") else "Tanpa keterangan",
                                      len(hd["tanpa_keterangan"]), ", ".join(hd["tanpa_keterangan"])))
        if hd["masuk_hari_libur"]:
            t.append("Masuk di hari libur: %s" % ", ".join(hd["masuk_hari_libur"]))
        if hd["lembur_disetujui"]:
            t.append("Lembur disetujui: %s" % ", ".join(
                ("%s %s jam" % (x["nama"], x["jam"])) if x["jam"] else (x["nama"] or "1 orang") for x in hd["lembur_disetujui"]))
    else:
        t.append("%d karyawan | hadir %d dari %d hari terjadwal" % (hd["karyawan"], hd["hari_hadir"], hd["hari_terjadwal"]))
        t.append("Terlambat %d kali (%d menit) | izin %d, sakit %d, cuti %d, dinas %d" % (
            hd["terlambat_kali"], hd["terlambat_menit"], hd["izin"], hd["sakit"], hd["cuti"], hd["dinas"]))
        t.append("Alpa %d | tanpa keterangan %d hari | lembur disetujui %s jam" % (
            hd["alpa"], hd["tanpa_keterangan"], hd["lembur_jam"]))
        if hd["sering_terlambat"]:
            t.append("Paling sering terlambat: " + ", ".join(
                "%s %dx" % (x["nama"], x["kali"]) for x in hd["sering_terlambat"]))
    if hd and hd["lembur_perlu_keputusan"]:
        t.append("Lembur perlu keputusan (belum disetujui):")
        for x in hd["lembur_perlu_keputusan"][:5]:
            tg_ = (" %s" % x["tanggal"][8:10] + "/" + x["tanggal"][5:7]) if x["tanggal"] else ""
            t.append("- %s%s: %s" % (x["nama"], tg_, x["pesan"].split(":")[0]))

    # Tagihan
    tg = data["tagihan"]
    t += ["", "TAGIHAN & FOLLOW-UP"]
    if not tg:
        t.append(pesan_kosong(A, "pengingat"))
    elif not (tg["terlambat"] or tg["hari_ini"] or tg["besok"]):
        t.append("Tidak ada yang terlambat, jatuh tempo hari ini, atau besok (%d item aktif)." % tg["jumlah_aktif"])
    else:
        t.append("Terlambat %d | hari ini %d | besok %d" % (len(tg["terlambat"]), len(tg["hari_ini"]), len(tg["besok"])))
        if tg["total_tertunggak"]:
            t.append("Piutang tertunggak (terlambat + hari ini): %s" % rp(tg["total_tertunggak"]))
        for x in (tg["terlambat"] + tg["hari_ini"] + tg["besok"])[:8]:
            t.append("- #%s %s%s, %s" % (x["id"], x["jenis"], (" " + rp(x["nominal"])) if x["nominal"] else "", x["keterangan"]))
        t.append("Nama & draf pesan: ketik \"rekap pengingat\".")

    # Prospek (CRM)
    pr = data["prospek"]
    t += ["", "PROSPEK"]
    if not pr:
        t.append(pesan_kosong(A, "crm"))
    else:
        f = pr["followup"]
        t.append("Prospek baru: %d" % pr["lead_masuk"])
        t.append("Follow-up terlambat %d | hari ini %d | besok %d | order perlu konfirmasi %d" % (
            f["terlambat"], f["hari_ini"], f["besok"], f["order_perlu_konfirmasi"]))
        if f["nilai_terlambat_dan_hari_ini"]:
            t.append("Nilai potensi (terlambat + hari ini): %s" % rp(f["nilai_terlambat_dan_hari_ini"]))
        dl = pr["deal"]
        t.append("Deal periode ini: %d senilai %s%s" % (
            dl["jumlah"], rp(dl["nilai"]), (" (%d belum diisi nilainya)" % dl["tanpa_nilai"]) if dl["tanpa_nilai"] else ""))
        ko = pr["kohort"]
        t.append("Konversi: %s (%d dari %d lead)" % (pr["konversi_teks"], ko["deal_atau_selesai"], ko["lead"]))
        sb = pr["sumber_terbaik"]
        if sb:
            t.append("Sumber lead terbaik: %s (%d lead, %d deal%s)" % (
                sb["sumber"], sb["lead"], sb["deal"], ", sampel kecil" if sb["sampel_kecil"] else ""))
        else:
            t.append("Sumber lead terbaik: belum ada deal dari lead periode ini.")
        if per["jenis"] == "mingguan":
            for nama, dari, sampai in per["banding"]:
                b = pr["banding"].get(nama)
                if not b:
                    continue
                if b["lead_masuk"] is None:
                    t.append("vs minggu sebelumnya: tidak ada data pembanding")
                else:
                    t.append("vs minggu sebelumnya: %d lead -> %s" % (b["lead_masuk"], b["teks_lead"]))
        t.append("Nama & nomor prospek: ketik \"follow-up hari ini\" atau \"rekap CRM\".")

    # Perhatian
    t += ["", "PERLU PERHATIAN"]
    if data["perhatian"]:
        t += ["%d. %s" % (i, s) for i, s in enumerate(data["perhatian"], 1)]
    else:
        t.append("Tidak ada.")
    sumber = [a["skill"] for a in A.values() if a["status"] == "ada"]
    t += ["", "Sumber: %s (hanya dibaca)." % (", ".join(sumber) if sumber else "belum ada alat terbaca")]
    return "\n".join(t)


def pesan_kosong(A, nama):
    a = A[nama]
    if a["status"] == "gagal":
        return "Belum ada data: %s tidak terbaca (lihat Perlu Perhatian)." % a["skill"]
    if a["status"] == "dilewati":
        return "Dilewati."
    return "Belum ada data (%s belum dipakai di komputer ini)." % a["skill"]


# --------------------------------------------------------------------------- main
class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen salah: %s\nContoh: laporan.py --periode harian --tanggal kemarin\n" % message)
        sys.exit(2)


def buat_parser():
    p = Parser(prog="laporan.py", description="Laporan harian/mingguan gabungan dari alat lokal Komunitech (hanya baca).")
    p.add_argument("--versi", action="version", version="laporan-harian-usaha " + VERSI)
    p.add_argument("--periode", choices=["harian", "mingguan"], default="harian")
    p.add_argument("--tanggal", help="harian: hari-ini (default) | kemarin | 2026-09-24 | 24/09/2026. "
                                     "mingguan: tanggal mana pun di minggu itu (default minggu lalu)")
    p.add_argument("--tz", default="Asia/Jakarta", help="Zona waktu (default Asia/Jakarta; WITA/WIT juga bisa)")
    p.add_argument("--json", action="store_true", help="Keluaran JSON (berisi juga 'teks')")
    p.add_argument("--samarkan", action="store_true", help="Nama karyawan ditampilkan sebagai inisial")
    p.add_argument("--maks-produk", type=int, default=5, help="Jumlah produk terlaris (default 5)")
    p.add_argument("--timeout", type=float, default=10.0, help="Detik menunggu database yang sedang dipakai (default 10)")
    p.add_argument("--tanpa", default="", help="Lewati alat, mis. 'absensi,pengingat,crm'")
    for n in ("kasir", "stok", "absensi", "crm"):
        p.add_argument("--%s-db" % n, help="Lokasi database %s (default sama dengan alatnya)" % ALAT[n]["skill"])
    p.add_argument("--pengingat", help="Lokasi pengingat/DAFTAR.csv (default: dicari di folder kerja)")
    for n in ALAT:
        p.add_argument("--%s-script" % n, help="Lokasi %s bila tidak ditemukan otomatis" % ALAT[n]["script"])
    p.add_argument("--sekarang", help=argparse.SUPPRESS)  # untuk uji: waktu acuan ISO
    return p


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        tanpa = {x.strip().lower() for x in (args.tanpa or "").split(",") if x.strip()}
        salah = tanpa - set(ALAT)
        if salah:
            raise ArgSalah("--tanpa hanya menerima: %s (bukan %s)" % (", ".join(ALAT), ", ".join(sorted(salah))))
        args.tanpa = tanpa
        if args.timeout <= 0 or args.maks_produk < 0:
            raise ArgSalah("--timeout harus > 0 dan --maks-produk >= 0")
        data = susun(args)
    except ArgSalah as e:
        if args.json:
            print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False, indent=2))
        else:
            sys.stderr.write("ERROR: %s\n" % e)
        return 2
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        print(data["teks"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
