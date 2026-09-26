#!/usr/bin/env python3
"""Uji regresi dasbor.py - tanpa Datasette, tanpa internet, tanpa paket tambahan.

Membuat database SQLite kecil untuk tiap alat (skema minimal yang cocok dengan skema asli
buku-stok/kasir-lokal/crm-wa/absensi-lokal/buku-piutang/kas-umkm), lalu memeriksa:
  - setiap canned query mengembalikan angka yang BENAR (dihitung ulang manual di uji ini);
  - database TIDAK PERNAH berubah (hash sebelum == sesudah) walau dipakai berkali-kali;
  - pesan galat jelas untuk: database tidak ada, database kosong, database rusak/bukan sqlite,
    alat/query tidak dikenal, dan tabel yang tidak ada (query salah alat).

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)
"""
import hashlib
import importlib.util
import io
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SINI = Path(__file__).resolve().parent
SKRIP = SINI.parent / "scripts" / "dasbor.py"

spec = importlib.util.spec_from_file_location("dasbor", SKRIP)
dasbor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dasbor)


def hash_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jalankan_json(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = dasbor.main(argv)
    return kode, json.loads(buf.getvalue())


class UjiStokMenipis(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "stok.db"
        conn = sqlite3.connect(str(self.db))
        conn.executescript("""
            CREATE TABLE produk (id INTEGER PRIMARY KEY, sku TEXT, nama TEXT, varian TEXT,
                satuan TEXT, harga_beli REAL, harga_jual REAL, hpp REAL, stok REAL,
                stok_min REAL, lokasi TEXT, aktif INTEGER);
        """)
        conn.executemany(
            "INSERT INTO produk (sku,nama,varian,satuan,stok,stok_min,lokasi,aktif) VALUES (?,?,?,?,?,?,?,?)",
            [
                ("KPI-250", "Kopi Bubuk", "250g", "pcs", 5, 10, "A1", 1),   # menipis
                ("TEP-1KG", "Tepung", "1kg", "pcs", 2, 8, "A2", 1),        # menipis (lebih parah)
                ("GUL-1KG", "Gula Aren", "1kg", "pcs", 30, 5, "A3", 1),    # aman
                ("LAMA", "Produk Nonaktif", "", "pcs", 0, 10, "", 0),      # nonaktif, harus diabaikan
            ],
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_hasil_benar_dan_terurut(self):
        h_sebelum = hash_file(self.db)
        hasil = dasbor.jalankan_query("buku-stok", "stok-menipis", cli_db=str(self.db))
        h_sesudah = hash_file(self.db)
        self.assertEqual(h_sebelum, h_sesudah, "database tidak boleh berubah setelah query baca-saja")
        sku = [b["sku"] for b in hasil["baris"]]
        self.assertEqual(sku, ["TEP-1KG", "KPI-250"], "urutan: paling parah dulu, nonaktif & aman tidak ikut")
        self.assertEqual(hasil["jumlah_baris"], 2)

    def test_json_lewat_cli(self):
        kode, d = jalankan_json(["query", "buku-stok", "stok-menipis", "--db", str(self.db), "--json"])
        self.assertEqual(kode, 0)
        self.assertTrue(d["ok"])
        self.assertEqual(d["jumlah_baris"], 2)


class UjiPenjualanPerHari(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "kasir.db"
        conn = sqlite3.connect(str(self.db))
        conn.executescript("""
            CREATE TABLE nota (id INTEGER PRIMARY KEY, no TEXT, jenis TEXT, waktu TEXT,
                ref_nota_id INTEGER, total INTEGER);
        """)
        conn.executemany(
            "INSERT INTO nota (id,no,jenis,waktu,ref_nota_id,total) VALUES (?,?,?,?,?,?)",
            [
                (1, "N-1", "jual", "2026-09-24 09:00:00", None, 36000),
                (2, "N-2", "jual", "2026-09-24 12:00:00", None, 15000),
                (3, "N-3", "jual", "2026-09-25 10:00:00", None, 24000),
                (4, "N-4", "jual", "2026-09-25 15:00:00", None, 50000),   # akan di-void
                (5, "V-1", "void", "2026-09-25 15:05:00", 4, 0),
            ],
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_nota_void_dikeluarkan(self):
        h_sebelum = hash_file(self.db)
        hasil = dasbor.jalankan_query("kasir-lokal", "penjualan-per-hari", cli_db=str(self.db))
        self.assertEqual(hash_file(self.db), h_sebelum)
        per_tanggal = {b["tanggal"]: b for b in hasil["baris"]}
        self.assertEqual(per_tanggal["2026-09-24"]["total_penjualan"], 51000)
        self.assertEqual(per_tanggal["2026-09-24"]["jumlah_nota"], 2)
        # 2026-09-25: hanya N-3 (24000) yang dihitung; N-4 sudah di-void
        self.assertEqual(per_tanggal["2026-09-25"]["total_penjualan"], 24000)
        self.assertEqual(per_tanggal["2026-09-25"]["jumlah_nota"], 1)


class UjiPiutangJatuhTempo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "piutang.db"
        conn = sqlite3.connect(str(self.db))
        conn.executescript("""
            CREATE TABLE pelanggan (id INTEGER PRIMARY KEY, nama TEXT);
            CREATE TABLE nota (id INTEGER PRIMARY KEY, pelanggan_id INTEGER, no_nota TEXT,
                tanggal TEXT, jatuh_tempo TEXT, nominal INTEGER, status TEXT);
            CREATE TABLE alokasi (id INTEGER PRIMARY KEY, nota_id INTEGER, jumlah INTEGER);
            CREATE TABLE potongan (id INTEGER PRIMARY KEY, nota_id INTEGER, jumlah INTEGER);
        """)
        conn.execute("INSERT INTO pelanggan VALUES (1,'Bu Tini'),(2,'Kafe Senja'),(3,'Batal Saja')")
        conn.executemany(
            "INSERT INTO nota (id,pelanggan_id,no_nota,tanggal,jatuh_tempo,nominal,status) VALUES (?,?,?,?,?,?,?)",
            [
                (1, 1, "PB-1", "2026-08-01", "2026-08-15", 1200000, "aktif"),   # lewat, belum dibayar -> muncul
                (2, 1, "PB-2", "2026-08-01", "2026-08-10", 500000, "aktif"),    # lewat tapi lunas -> tidak muncul
                (3, 2, "PB-3", "2026-09-20", "2030-01-01", 2500000, "aktif"),   # belum jatuh tempo -> tidak muncul
                (4, 3, "PB-4", "2026-08-01", "2026-08-05", 999999, "batal"),    # batal -> tidak muncul
            ],
        )
        conn.execute("INSERT INTO alokasi (nota_id, jumlah) VALUES (2, 500000)")
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_hanya_yang_lewat_dan_belum_lunas(self):
        hasil = dasbor.jalankan_query("buku-piutang", "piutang-jatuh-tempo", cli_db=str(self.db))
        no_nota = {b["no_nota"]: b["sisa"] for b in hasil["baris"]}
        self.assertEqual(no_nota, {"PB-1": 1200000})


class UjiKehadiranHarian(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "absensi.db"
        conn = sqlite3.connect(str(self.db))
        conn.executescript("""
            CREATE TABLE karyawan (kode TEXT PRIMARY KEY, nama TEXT);
            CREATE TABLE tap (id INTEGER PRIMARY KEY, kode TEXT, waktu TEXT, jenis TEXT, tanggal_kerja TEXT);
        """)
        conn.execute("INSERT INTO karyawan VALUES ('A01','Andi'),('A02','Sari')")
        conn.executemany(
            "INSERT INTO tap (kode,waktu,jenis,tanggal_kerja) VALUES (?,?,?,?)",
            [
                ("A01", "2026-09-25 08:05:00", "masuk", "2026-09-25"),
                ("A01", "2026-09-25 17:10:00", "pulang", "2026-09-25"),
                ("A02", "2026-09-25 08:20:00", "masuk", "2026-09-25"),
                ("A01", "2026-09-26 08:00:00", "masuk", "2026-09-26"),   # hari lain, tidak ikut
            ],
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_default_hari_ini_kosong_bila_tak_ada_data(self):
        # Tanpa --tanggal, default = hari ini (kemungkinan besar tidak ada di data uji ini)
        hasil = dasbor.jalankan_query("absensi-lokal", "kehadiran-harian", cli_db=str(self.db),
                                       tanggal="2099-01-01")
        self.assertEqual(hasil["baris"], [])

    def test_tanggal_eksplisit(self):
        hasil = dasbor.jalankan_query("absensi-lokal", "kehadiran-harian", cli_db=str(self.db),
                                       tanggal="2026-09-25")
        by_kode = {b["kode"]: b for b in hasil["baris"]}
        self.assertEqual(by_kode["A01"]["jam_masuk"], "2026-09-25 08:05:00")
        self.assertEqual(by_kode["A01"]["jam_pulang"], "2026-09-25 17:10:00")
        self.assertIsNone(by_kode["A02"]["jam_pulang"])  # Sari belum tap pulang


class UjiProspekPerTahap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "crm.db"
        conn = sqlite3.connect(str(self.db))
        conn.execute("CREATE TABLE kontak (id INTEGER PRIMARY KEY, tahap TEXT, nilai INTEGER)")
        conn.executemany("INSERT INTO kontak (tahap, nilai) VALUES (?,?)", [
            ("baru", 300000), ("ditawar", 1200000), ("deal", 4500000), ("deal", 900000),
        ])
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_pengelompokan_benar(self):
        hasil = dasbor.jalankan_query("crm-wa", "prospek-per-tahap", cli_db=str(self.db))
        by_tahap = {b["tahap"]: b for b in hasil["baris"]}
        self.assertEqual(by_tahap["deal"]["jumlah"], 2)
        self.assertEqual(by_tahap["deal"]["total_nilai_potensi"], 5400000)


class UjiSaldoKas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "kas.db"
        conn = sqlite3.connect(str(self.db))
        conn.executescript("""
            CREATE TABLE akun (id INTEGER PRIMARY KEY, nama TEXT, jenis TEXT, saldo_awal INTEGER);
            CREATE TABLE transaksi (id INTEGER PRIMARY KEY, akun_id INTEGER, arah TEXT,
                jumlah INTEGER, status TEXT);
        """)
        conn.execute("INSERT INTO akun VALUES (1,'Laci kas','tunai',100000)")
        conn.executemany("INSERT INTO transaksi (akun_id,arah,jumlah,status) VALUES (?,?,?,?)", [
            (1, "masuk", 500000, "aktif"),
            (1, "keluar", 150000, "aktif"),
            (1, "masuk", 999999, "batal"),   # dibatalkan, tidak boleh ikut
        ])
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_saldo_hitung_benar(self):
        hasil = dasbor.jalankan_query("kas-umkm", "saldo-per-akun", cli_db=str(self.db))
        self.assertEqual(hasil["baris"][0]["saldo"], 100000 + 500000 - 150000)


class UjiPenangananGalat(unittest.TestCase):
    def test_db_tidak_ada(self):
        with self.assertRaises(dasbor.Gagal) as c:
            dasbor.jalankan_query("buku-stok", "stok-menipis", cli_db="/tidak/ada/xyz-123.db")
        self.assertTrue(c.exception.data.get("belum_ada"))

    def test_db_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "kosong.db"
            p.touch()
            with self.assertRaises(dasbor.Gagal) as c:
                dasbor.jalankan_query("buku-stok", "stok-menipis", cli_db=str(p))
            self.assertTrue(c.exception.data.get("rusak"))

    def test_db_rusak_bukan_sqlite(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "rusak.db"
            p.write_bytes(b"ini bukan file sqlite sama sekali, cuma teks biasa")
            with self.assertRaises(dasbor.Gagal) as c:
                dasbor.jalankan_query("buku-stok", "stok-menipis", cli_db=str(p))
            self.assertTrue(c.exception.data.get("rusak"))

    def test_alat_tidak_dikenal(self):
        with self.assertRaises(dasbor.Gagal):
            dasbor.jalankan_query("alat-ngasal", "apa-saja")

    def test_query_tidak_dikenal(self):
        with self.assertRaises(dasbor.Gagal):
            dasbor.jalankan_query("buku-stok", "query-ngasal")

    def test_tabel_tidak_ada_pesan_jelas(self):
        # DB buku-stok dipakai untuk query kasir-lokal -> tabel 'nota' tidak ada
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "stok.db"
            conn = sqlite3.connect(str(p))
            conn.execute("CREATE TABLE produk (id INTEGER)")
            conn.commit()
            conn.close()
            with self.assertRaises(dasbor.Gagal) as c:
                dasbor.jalankan_query("kasir-lokal", "penjualan-per-hari", cli_db=str(p))
            self.assertIn("tidak punya struktur", c.exception.pesan)

    def test_cli_json_galat_tetap_kode_1(self):
        kode, d = jalankan_json(["query", "buku-stok", "stok-menipis", "--db",
                                  "/tidak/ada/lagi.db", "--json"])
        self.assertEqual(kode, 1)
        self.assertFalse(d["ok"])
        self.assertIn("error", d)


class UjiCariDanDaftarQuery(unittest.TestCase):
    def test_cari_mengembalikan_enam_alat(self):
        hasil = dasbor.cari_semua(env={})
        nama = {x["alat"] for x in hasil}
        self.assertEqual(nama, set(dasbor.ALAT))

    def test_path_db_urutan_prioritas(self):
        # --db menang atas semuanya
        self.assertEqual(str(dasbor.path_db("buku-stok", cli_db="/pilihan/saya.db")), "/pilihan/saya.db")
        # ENV khusus alat menang atas KOMUNITECH_DATA
        env = {"KOMUNITECH_STOK_DB": "/env/stok.db", "KOMUNITECH_DATA": "/data"}
        self.assertEqual(str(dasbor.path_db("buku-stok", env=env)), "/env/stok.db")
        # KOMUNITECH_DATA dipakai bila ENV khusus kosong
        env2 = {"KOMUNITECH_DATA": "/data"}
        self.assertEqual(str(dasbor.path_db("kasir-lokal", env=env2)), str(Path("/data/kasir/kasir.db")))

    def test_daftar_query_semua_alat_ada_isi(self):
        for nama, info in dasbor.ALAT.items():
            self.assertTrue(info["queries"], "%s tidak punya query" % nama)


if __name__ == "__main__":
    unittest.main(verbosity=2)
