#!/usr/bin/env python3
"""dasbor-lokal (Komunitech) - jembatan baca-saja ke database alat lokal Komunitech.

Membantu menemukan file SQLite alat lokal (buku-stok, kasir-lokal, crm-wa, absensi-lokal,
buku-piutang, kas-umkm), menjalankan "canned query" siap pakai (penjualan per hari, stok
menipis, piutang jatuh tempo, kehadiran, prospek per tahap, saldo kas), dan menyiapkan
perintah Datasette (jika terpasang) untuk eksplorasi interaktif di browser.

TIDAK PERNAH menulis ke database alat lain: semua koneksi dibuka lewat URI SQLite
"?mode=ro" (baca-saja pada level driver). Hanya library standar Python 3.8+, lintas OS
(Windows: `python`/`py`), tanpa akses jaringan.

Lokasi database tiap alat (urutan prioritas, sama seperti skill masing-masing):
  1. --db PATH
  2. ENV khusus alat (mis. KOMUNITECH_STOK_DB) - path file lengkap
  3. ENV KOMUNITECH_DATA (folder bersama) + sub-path alat itu
  4. ~/KomunitechData/<sub-path default>

Contoh:
  python3 dasbor.py cari
  python3 dasbor.py daftar-query
  python3 dasbor.py query kasir-lokal penjualan-per-hari
  python3 dasbor.py query buku-piutang piutang-jatuh-tempo --json
  python3 dasbor.py query absensi-lokal kehadiran-harian --tanggal 2026-09-25
  python3 dasbor.py datasette

Kode keluar: 0 = berhasil; 1 = gagal (pesan jelas di "error"/stderr); 2 = perintah salah tulis.
"""
import argparse
import json
import shutil
import sqlite3
import sys
from datetime import date
from pathlib import Path

APLIKASI = "dasbor-lokal"
VERSI = "1.0.0"
FOLDER_SKRIP = Path(__file__).resolve().parent
FOLDER_SKILL = FOLDER_SKRIP.parent


class Gagal(Exception):
    def __init__(self, pesan, **kw):
        super().__init__(pesan)
        self.pesan = pesan
        self.data = kw


class Query:
    def __init__(self, judul, sql, tabel, butuh_tanggal=False):
        self.judul = judul
        self.sql = sql
        self.tabel = tabel          # tabel yang wajib ada, untuk pesan galat yang jelas
        self.butuh_tanggal = butuh_tanggal


# --- Definisi setiap alat lokal Komunitech --------------------------------------------
ALAT = {
    "buku-stok": {
        "env_db": "KOMUNITECH_STOK_DB",
        "sub": "stok.db",
        "queries": {
            "stok-menipis": Query(
                "Stok menipis atau habis",
                """SELECT sku, nama, varian, satuan, stok, stok_min, lokasi
                   FROM produk
                   WHERE aktif = 1 AND stok <= stok_min
                   ORDER BY (stok - stok_min) ASC""",
                tabel="produk",
            ),
        },
    },
    "kasir-lokal": {
        "env_db": "KOMUNITECH_KASIR_DB",
        "sub": "kasir/kasir.db",
        "queries": {
            "penjualan-per-hari": Query(
                "Penjualan per hari (30 hari terakhir, nota void dikeluarkan)",
                """SELECT date(waktu) AS tanggal, COUNT(*) AS jumlah_nota, SUM(total) AS total_penjualan
                   FROM nota
                   WHERE jenis = 'jual'
                     AND id NOT IN (SELECT ref_nota_id FROM nota
                                    WHERE jenis = 'void' AND ref_nota_id IS NOT NULL)
                     AND date(waktu) >= date('now', '-30 days')
                   GROUP BY date(waktu)
                   ORDER BY tanggal DESC""",
                tabel="nota",
            ),
        },
    },
    "crm-wa": {
        "env_db": "KOMUNITECH_CRM_DB",
        "sub": "crm/crm.db",
        "queries": {
            "prospek-per-tahap": Query(
                "Jumlah & nilai prospek per tahap pipeline",
                """SELECT tahap, COUNT(*) AS jumlah, SUM(nilai) AS total_nilai_potensi
                   FROM kontak
                   GROUP BY tahap
                   ORDER BY jumlah DESC""",
                tabel="kontak",
            ),
        },
    },
    "absensi-lokal": {
        "env_db": "KOMUNITECH_ABSENSI_DB",
        "sub": "absensi/absensi.db",
        "queries": {
            "kehadiran-harian": Query(
                "Jam masuk/pulang per karyawan pada satu tanggal (default hari ini)",
                """SELECT k.kode, k.nama, t.tanggal_kerja,
                          MIN(CASE WHEN t.jenis = 'masuk' THEN t.waktu END) AS jam_masuk,
                          MAX(CASE WHEN t.jenis = 'pulang' THEN t.waktu END) AS jam_pulang
                   FROM tap t
                   JOIN karyawan k ON k.kode = t.kode
                   WHERE t.tanggal_kerja = :tanggal
                   GROUP BY k.kode
                   ORDER BY k.nama""",
                tabel="tap",
                butuh_tanggal=True,
            ),
        },
    },
    "buku-piutang": {
        "env_db": "KOMUNITECH_PIUTANG_DB",
        "sub": "piutang/piutang.db",
        "queries": {
            "piutang-jatuh-tempo": Query(
                "Piutang jatuh tempo atau sudah terlewat (sisa > 0)",
                """SELECT * FROM (
                     SELECT p.nama AS pelanggan, n.no_nota, n.tanggal, n.jatuh_tempo,
                            n.nominal
                              - COALESCE((SELECT SUM(jumlah) FROM alokasi WHERE nota_id = n.id), 0)
                              - COALESCE((SELECT SUM(jumlah) FROM potongan WHERE nota_id = n.id), 0) AS sisa
                     FROM nota n JOIN pelanggan p ON p.id = n.pelanggan_id
                     WHERE n.status = 'aktif'
                   )
                   WHERE sisa > 0 AND date(jatuh_tempo) <= date('now')
                   ORDER BY jatuh_tempo ASC""",
                tabel="nota",
            ),
        },
    },
    "kas-umkm": {
        "env_db": "KOMUNITECH_KAS_DB",
        "sub": "kas/kas.db",
        "queries": {
            "saldo-per-akun": Query(
                "Saldo kas per akun (laci, bank, e-wallet, ...)",
                """SELECT a.nama AS akun, a.jenis,
                          a.saldo_awal
                            + COALESCE((SELECT SUM(jumlah) FROM transaksi
                                        WHERE akun_id = a.id AND arah = 'masuk' AND status = 'aktif'), 0)
                            - COALESCE((SELECT SUM(jumlah) FROM transaksi
                                        WHERE akun_id = a.id AND arah = 'keluar' AND status = 'aktif'), 0) AS saldo
                   FROM akun a
                   ORDER BY a.nama""",
                tabel="akun",
            ),
        },
    },
}

KOLOM_UANG = {"total_penjualan", "sisa", "nominal", "total_nilai_potensi", "saldo",
              "harga_jual", "harga_beli", "hpp"}


def path_default(nama_alat):
    return Path.home() / "KomunitechData" / ALAT[nama_alat]["sub"]


def path_db(nama_alat, cli_db=None, env=None):
    """Urutan prioritas identik dengan skill aslinya masing-masing."""
    import os
    env = env or os.environ
    if cli_db:
        return Path(cli_db).expanduser()
    info = ALAT[nama_alat]
    if env.get(info["env_db"]):
        return Path(env[info["env_db"]]).expanduser()
    if env.get("KOMUNITECH_DATA"):
        return Path(env["KOMUNITECH_DATA"]).expanduser() / info["sub"]
    return path_default(nama_alat)


def cari_semua(env=None):
    hasil = []
    for nama in ALAT:
        p = path_db(nama, env=env)
        hasil.append({"alat": nama, "db": str(p), "ada": p.is_file(),
                      "ukuran_kb": round(p.stat().st_size / 1024, 1) if p.is_file() else None})
    return hasil


def buka_baca_saja(db):
    """Sambungkan ke SQLite lewat URI '?mode=ro': gagal (bukan menunggu) jika file tidak ada,
    dan level driver menolak semua tulisan meski SQL-nya bukan SELECT."""
    if not db.is_file():
        raise Gagal(
            "Database tidak ditemukan di %s. Pastikan alat itu sudah pernah dipakai (ada datanya), "
            "atau tunjukkan lokasinya dengan --db PATH. Lihat docs/panduan-datasette.md." % db,
            db=str(db), belum_ada=True)
    if db.stat().st_size == 0:
        raise Gagal("File %s kosong (0 byte), bukan database yang bisa dibaca." % db, db=str(db), rusak=True)
    try:
        conn = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=5)
    except sqlite3.OperationalError as e:
        raise Gagal("Database %s tidak bisa dibuka (%s). Periksa izin akses filenya." % (db, e), db=str(db))
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("SELECT 1")
    except sqlite3.DatabaseError as e:
        conn.close()
        raise Gagal("File %s bukan database SQLite yang valid atau rusak (%s)." % (db, e), db=str(db), rusak=True)
    return conn


def jalankan_query(nama_alat, nama_query, cli_db=None, tanggal=None):
    if nama_alat not in ALAT:
        raise Gagal("Alat '%s' tidak dikenal. Pilihan: %s" % (nama_alat, ", ".join(sorted(ALAT))))
    q = ALAT[nama_alat]["queries"].get(nama_query)
    if not q:
        raise Gagal("Query '%s' tidak ada untuk %s. Pilihan: %s" %
                     (nama_query, nama_alat, ", ".join(sorted(ALAT[nama_alat]["queries"]))))
    db = path_db(nama_alat, cli_db)
    conn = buka_baca_saja(db)
    try:
        param = {}
        if q.butuh_tanggal:
            param["tanggal"] = tanggal or date.today().isoformat()
        try:
            baris = [dict(r) for r in conn.execute(q.sql, param).fetchall()]
        except sqlite3.DatabaseError as e:
            pesan = str(e)
            if "no such table" in pesan or "no such column" in pesan:
                raise Gagal(
                    "Database %s tidak punya struktur yang diharapkan untuk %s (%s). Mungkin file ini "
                    "bukan database %s, atau versinya sudah usang. Perbarui skill %s lalu coba lagi." %
                    (db, nama_query, pesan, nama_alat, nama_alat), db=str(db))
            if "database is locked" in pesan:
                raise Gagal(
                    "Database %s sedang dipakai program lain. Data aman; tunggu sebentar lalu coba lagi." % db,
                    db=str(db))
            if "file is not a database" in pesan or "not a database" in pesan or "malformed" in pesan:
                raise Gagal("File %s bukan database SQLite yang valid atau rusak (%s)." % (db, pesan),
                             db=str(db), rusak=True)
            raise Gagal("Gagal menjalankan query di %s: %s" % (db, pesan), db=str(db))
        return {"alat": nama_alat, "query": nama_query, "judul": q.judul, "db": str(db),
                "parameter": param, "jumlah_baris": len(baris), "baris": baris}
    finally:
        conn.close()


def fmt_nilai(kolom, nilai):
    if nilai is None:
        return ""
    if kolom in KOLOM_UANG and isinstance(nilai, (int, float)):
        return "Rp " + "{:,.0f}".format(nilai).replace(",", ".")
    return str(nilai)


def cetak_tabel(hasil):
    baris = hasil["baris"]
    print("=== %s / %s: %s ===" % (hasil["alat"], hasil["query"], hasil["judul"]))
    print("Sumber: %s" % hasil["db"])
    if not baris:
        print("(tidak ada data yang cocok)")
        return
    kolom = list(baris[0].keys())
    lebar = {k: max(len(k), *(len(fmt_nilai(k, b.get(k))) for b in baris)) for k in kolom}
    print(" | ".join(k.ljust(lebar[k]) for k in kolom))
    print("-+-".join("-" * lebar[k] for k in kolom))
    for b in baris:
        print(" | ".join(fmt_nilai(k, b.get(k)).ljust(lebar[k]) for k in kolom))
    print("(%d baris)" % len(baris))


def cetak_perintah_datasette(env=None):
    ada = [x for x in cari_semua(env) if x["ada"]]
    exe = shutil.which("datasette")
    templat = FOLDER_SKILL / "templates" / "metadata.yml"
    baris = []
    if not exe:
        baris.append("Datasette belum terpasang di komputer ini.")
        baris.append("Pasang sekali (lihat docs/panduan-datasette.md): pipx install datasette")
        baris.append("(Skill ini tetap berguna tanpa Datasette lewat perintah 'query' di atas.)")
        baris.append("")
    baris.append("Perintah yang disarankan (localhost saja, semua database read-only/immutable):")
    if not ada:
        baris.append("(belum ada database alat lokal yang ditemukan; jalankan alatnya dulu)")
    else:
        bagian = ["datasette"]
        for x in ada:
            bagian.append('-i "%s"' % x["db"])
        if templat.is_file():
            bagian.append('-m "%s"' % templat)
        bagian.append("--host 127.0.0.1")
        baris.append(" \\\n  ".join(bagian))
    return "\n".join(baris)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="dasbor.py", description="Dasbor lokal Komunitech (baca-saja)")
    ap.add_argument("--versi", action="version", version="%s %s" % (APLIKASI, VERSI))
    sub = ap.add_subparsers(dest="perintah")

    p_cari = sub.add_parser("cari", help="Temukan file database tiap alat lokal")
    p_cari.add_argument("--json", action="store_true")

    p_daftar = sub.add_parser("daftar-query", help="Daftar query siap pakai per alat")
    p_daftar.add_argument("--json", action="store_true")

    p_q = sub.add_parser("query", help="Jalankan satu query siap pakai")
    p_q.add_argument("alat", choices=sorted(ALAT))
    p_q.add_argument("query")
    p_q.add_argument("--db", help="Path database (mengganti lokasi default/ENV)")
    p_q.add_argument("--tanggal", help="YYYY-MM-DD (untuk query yang butuh tanggal, default hari ini)")
    p_q.add_argument("--json", action="store_true")

    p_ds = sub.add_parser("datasette", help="Cetak perintah Datasette read-only untuk semua database yang ada")
    p_ds.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)
    if not args.perintah:
        ap.print_help()
        return 2

    try:
        if args.perintah == "cari":
            hasil = cari_semua()
            if args.json:
                print(json.dumps({"ok": True, "alat": hasil}, ensure_ascii=False, indent=2))
            else:
                for x in hasil:
                    tanda = "ADA   " if x["ada"] else "TIDAK ADA"
                    ukuran = (" (%s KB)" % x["ukuran_kb"]) if x["ada"] else ""
                    print("%-14s %-9s %s%s" % (x["alat"], tanda, x["db"], ukuran))
            return 0

        if args.perintah == "daftar-query":
            data = {a: {q: v.judul for q, v in info["queries"].items()} for a, info in ALAT.items()}
            if args.json:
                print(json.dumps({"ok": True, "query": data}, ensure_ascii=False, indent=2))
            else:
                for a, qs in data.items():
                    print(a + ":")
                    for q, judul in qs.items():
                        print("  - %s : %s" % (q, judul))
            return 0

        if args.perintah == "query":
            hasil = jalankan_query(args.alat, args.query, cli_db=args.db, tanggal=args.tanggal)
            if args.json:
                print(json.dumps({"ok": True, **hasil}, ensure_ascii=False, indent=2, default=str))
            else:
                cetak_tabel(hasil)
            return 0

        if args.perintah == "datasette":
            teks = cetak_perintah_datasette()
            if args.json:
                print(json.dumps({"ok": True, "petunjuk": teks}, ensure_ascii=False, indent=2))
            else:
                print(teks)
            return 0
    except Gagal as e:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": e.pesan, **e.data}, ensure_ascii=False, indent=2))
        else:
            print("GAGAL: %s" % e.pesan, file=sys.stderr)
        return 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
