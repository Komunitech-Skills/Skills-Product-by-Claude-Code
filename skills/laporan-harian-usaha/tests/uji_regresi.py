#!/usr/bin/env python3
"""Uji regresi laporan-harian-usaha.

Data contoh DIBUAT dengan menjalankan script alat asli (kasir-lokal, buku-stok, absensi-lokal,
pengingat-follow-up, crm-wa) di folder sementara, bukan meniru skema dengan tangan. Alat dicari di folder
skills yang sama (../kasir-lokal, dst.); jika tidak ada, uji yang membutuhkannya dilewati.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import csv
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
SKILLS = SINI.parent
LAPORAN = SINI / "scripts" / "laporan.py"
KASIR = SKILLS / "kasir-lokal" / "scripts" / "kasir.py"
STOK = SKILLS / "buku-stok" / "scripts" / "stok.py"
ABSENSI = SKILLS / "absensi-lokal" / "scripts" / "absensi.py"
PENGINGAT = SKILLS / "pengingat-follow-up" / "scripts" / "cek_jatuh_tempo.py"
DAFTAR_CONTOH = SKILLS / "pengingat-follow-up" / "templates" / "DAFTAR.csv"
CRM = SKILLS / "crm-wa" / "scripts" / "crm.py"
SEMUA_ALAT = all(p.is_file() for p in (KASIR, STOK, ABSENSI, PENGINGAT, DAFTAR_CONTOH, CRM))
SEKARANG = "2026-09-24T21:00:00+07:00"

sys.path.insert(0, str(SINI / "scripts"))
import laporan  # noqa: E402


def alat(script, *argv, data=None):
    env = dict(os.environ)
    env["KOMUNITECH_DATA"] = str(data)
    env.pop("KOMUNITECH_KASIR_DB", None)
    env.pop("KOMUNITECH_STOK_DB", None)
    env.pop("KOMUNITECH_ABSENSI_DB", None)
    env.pop("KOMUNITECH_CRM_DB", None)
    p = subprocess.run([sys.executable, str(script)] + [str(a) for a in argv], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=env)
    if p.returncode != 0:
        raise AssertionError("alat gagal: %s %s\n%s\n%s" % (script.name, argv, p.stdout.decode(), p.stderr.decode()))
    return json.loads(p.stdout.decode()) if p.stdout.strip().startswith(b"{") else p.stdout.decode()


def buat_data(akar):
    """Isi folder akar/data (+ akar/kerja/pengingat) dengan alat asli."""
    data = akar / "data"
    data.mkdir(parents=True)
    H = ["--hari-ini", "2026-09-24T21:00"]
    K = lambda *a: alat(KASIR, *(list(a) + ["--json"] + H), data=data)  # noqa: E731
    K("init", "--nama-toko", "Warung Uji", "--stok", "buku-stok", "--ya")
    K("produk", "impor", SKILLS / "kasir-lokal" / "templates" / "produk-contoh.csv", "--ya")
    K("jual", "--pesan", "1 kopi hitam, bayar tunai", "--waktu", "2026-09-17 10:00", "--ya")
    K("jual", "--pesan", "2 kopi susu, bayar tunai 50rb", "--waktu", "2026-09-23 10:00", "--ya")
    K("buka-kasir", "--kas-awal", "200rb", "--waktu", "2026-09-24 07:00", "--ya")
    K("jual", "--pesan", "2 kopi susu, 1 roti bakar, bayar tunai 100rb", "--waktu", "2026-09-24 09:00", "--ya")
    K("jual", "--pesan", "3 es teh manis, bayar qris", "--waktu", "2026-09-24 12:00", "--ya")
    K("jual", "--pesan", "1 kopi hitam, bayar tunai", "--waktu", "2026-09-24 13:00", "--ya")
    K("void", "--nota", "N-260924-0003", "--alasan", "salah input", "--waktu", "2026-09-24 13:05", "--ya")
    K("tutup-kasir", "--kas-fisik", "240000", "--waktu", "2026-09-24 20:00", "--ya")

    T = lambda *a: alat(STOK, *(list(a) + ["--json"]), data=data)  # noqa: E731
    T("init", "--ya")
    csvp = akar / "produk-stok.csv"
    csvp.write_text("SKU;Nama Produk;Varian;Satuan;Harga Beli;Harga Jual;Stok;Stok Minimum;Lokasi\n"
                    "KSGA;Kopi Susu Gula Aren;;cup;8000;18000;30;10;A1\n"
                    "KH;Kopi Hitam;;cup;5000;12000;4;10;A1\n"
                    "ETM;Es Teh Manis;;gelas;2000;6000;0;5;A2\n"
                    "RB;Roti Bakar;Coklat;porsi;7000;15000;20;5;B1\n", encoding="utf-8")
    T("produk", "impor", csvp, "--tanggal", "2026-09-01", "--ya")
    jual23 = akar / "jual23.csv"
    K("ekspor", "--format", "buku-stok", "--tanggal", "2026-09-23", "--csv", jual23)
    T("impor-pesanan", jual23, "--platform", "lainnya", "--ya")  # hanya tgl 23 yang diimpor
    T("keluar", "--sku", "RB", "--qty", "25", "--izinkan-minus", "--tanggal", "2026-09-24", "--ya")

    N = ["--sekarang", "2026-09-24T21:00"]
    A = lambda *a: alat(ABSENSI, *(list(a) + ["--json"] + N), data=data)  # noqa: E731
    A("init", "--ya")
    for kode, nama in (("A01", "Andi"), ("A02", "Sari"), ("A03", "Budi"), ("A04", "Rina"), ("A05", "Joko")):
        A("karyawan", "tambah", "--kode", kode, "--nama", nama, "--mulai", "2026-09-01", "--ya")
    A("catat", "--karyawan", "Andi", "--tanggal", "2026-09-24", "--masuk", "08.12", "--pulang", "18.10", "--ya")
    A("catat", "--karyawan", "Sari", "--tanggal", "2026-09-24", "--masuk", "07.55", "--pulang", "19.30", "--ya")
    A("keterangan", "--karyawan", "Budi", "--jenis", "sakit", "--tanggal", "2026-09-24", "--ya")
    A("keterangan", "--karyawan", "Rina", "--jenis", "alpa", "--tanggal", "2026-09-24", "--ya")
    A("lembur", "--karyawan", "Andi", "--tanggal", "2026-09-24", "--jam", "1", "--catatan", "disetujui Bu Maya", "--ya")

    (akar / "kerja" / "pengingat").mkdir(parents=True)
    shutil.copyfile(str(DAFTAR_CONTOH), str(akar / "kerja" / "pengingat" / "DAFTAR.csv"))

    # crm-wa: 5 prospek dengan tanggal masuk/follow-up/deal berbeda, dipakai untuk verifikasi PROSPEK
    # (angka dicocokkan dengan `crm.py rekap --json` langsung di uji, bukan ditebak).
    HC = ["--json", "--hari-ini", "2026-09-24"]
    C = lambda *a: alat(CRM, *(list(a) + HC), data=data)  # noqa: E731
    C("init", "--nama-usaha", "Warung Uji", "--pengirim", "Sari", "--zona", "WIB", "--ya")
    C("tambah", "--nama", "Bu Rina", "--wa", "0812-3000-0001", "--sumber", "ig", "--tahap", "dihubungi",
      "--masuk", "2026-09-20", "--followup", "2026-09-22")                                  # terlambat 2 hari
    C("tambah", "--nama", "Pak Budi", "--wa", "0812-3000-0002", "--sumber", "tiktok", "--tahap", "ditawar",
      "--nilai", "4,5 jt", "--masuk", "2026-09-23", "--followup", "2026-09-24")              # follow-up hari ini
    C("tambah", "--nama", "Bu Sari Toko", "--wa", "0812-3000-0003", "--sumber", "ig", "--tahap", "ditawar",
      "--masuk", "2026-09-18")
    C("catat", "--kontak", "Bu Sari Toko", "--tahap", "deal", "--nilai", "6 jt", "--tanggal", "2026-09-24")
    C("tambah", "--nama", "Mbak Dewi", "--wa", "0812-3000-0005", "--sumber", "tokopedia", "--tahap", "baru",
      "--masuk", "2026-09-24")                                                              # follow-up hari ini
    C("tambah", "--nama", "Mas Andi", "--wa", "0812-3000-0006", "--sumber", "ig", "--tahap", "ditawar",
      "--masuk", "2026-09-22")
    C("catat", "--kontak", "Mas Andi", "--tahap", "deal", "--nilai", "2 jt", "--tanggal", "2026-09-23")


def md5_folder(fol):
    h = {}
    for p in sorted(Path(fol).rglob("*")):
        if p.is_file():
            h[str(p.relative_to(fol))] = hashlib.md5(p.read_bytes()).hexdigest()
    return h


class Dasar(unittest.TestCase):
    master = None

    @classmethod
    def setUpClass(cls):
        cls.tmp_induk = Path(tempfile.mkdtemp(prefix="uji-laporan-usaha-"))
        if SEMUA_ALAT and Dasar.master is None:
            Dasar.master = Path(tempfile.mkdtemp(prefix="uji-laporan-master-")) / "m"
            buat_data(Dasar.master)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(str(cls.tmp_induk), ignore_errors=True)

    def salin(self, nama):
        tujuan = self.tmp_induk / nama
        shutil.copytree(str(Dasar.master), str(tujuan))
        return tujuan

    def kosong(self, nama):
        tujuan = self.tmp_induk / nama
        (tujuan / "data").mkdir(parents=True)
        (tujuan / "kerja").mkdir()
        return tujuan

    def jalan(self, akar, *argv, tz="Asia/Jakarta", env_tambah=None, harap_kode=0):
        env = {k: v for k, v in os.environ.items() if not k.startswith("KOMUNITECH_")}
        env.update({"HOME": str(akar), "USERPROFILE": str(akar), "KOMUNITECH_DATA": str(akar / "data"),
                    "PYTHONIOENCODING": "utf-8"})
        if tz:
            env["TZ"] = tz
        env.update(env_tambah or {})
        argv = list(argv)
        if "--sekarang" not in argv:
            argv += ["--sekarang", SEKARANG]
        mulai = time.time()
        p = subprocess.run([sys.executable, str(LAPORAN)] + argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=env, cwd=str(akar / "kerja"))
        self.durasi = time.time() - mulai
        out, err = p.stdout.decode("utf-8"), p.stderr.decode("utf-8")
        self.assertEqual(p.returncode, harap_kode, "kode keluar %d\nSTDOUT:\n%s\nSTDERR:\n%s" % (p.returncode, out, err))
        if "--json" in argv and p.returncode == 0:
            return json.loads(out)
        return out + err


# ------------------------------------------------------------------ uji fungsi murni (tanpa alat)
class UjiRumus(unittest.TestCase):
    def test_persen_pembagi_nol(self):
        self.assertEqual(laporan.persen(50000, 0), (None, "naik dari Rp 0 (persen tidak dihitung)"))
        self.assertEqual(laporan.persen(0, 0), (None, "sama-sama Rp 0"))

    def test_persen_pembanding_minus_dan_kosong(self):
        self.assertEqual(laporan.persen(1000, -500)[0], None)
        self.assertEqual(laporan.persen(1000, None), (None, "tidak ada data pembanding"))

    def test_persen_pembulatan_setengah_ke_atas(self):
        # (2001-2000)/2000*100 = 0,05 -> 0,1 ; (1999-2000)/2000*100 = -0,05 -> -0,1 (menjauhi nol)
        self.assertEqual(laporan.persen(2001, 2000), ("0.1", "naik 0,1%"))
        self.assertEqual(laporan.persen(1999, 2000), ("-0.1", "turun 0,1%"))
        self.assertEqual(laporan.persen(1000, 3000), ("-66.7", "turun 66,7%"))
        self.assertEqual(laporan.persen(5000, 5000), ("0.0", "sama (0%)"))

    def test_format_rupiah(self):
        self.assertEqual(laporan.rp(1250000), "Rp 1.250.000")
        self.assertEqual(laporan.rp(-12000), "-Rp 12.000")
        self.assertEqual(laporan.fq("1.5"), "1,5")

    def test_zona_waktu_tengah_malam(self):
        a = laporan.buat_parser().parse_args(["--sekarang", "2026-09-24T17:30:00Z"])
        tz = laporan.zona("Asia/Jakarta")[0]
        self.assertEqual(laporan.waktu_sekarang(a, tz).date().isoformat(), "2026-09-25")  # 00.30 WIB
        a = laporan.buat_parser().parse_args(["--sekarang", "2026-09-24T16:59:00Z"])
        self.assertEqual(laporan.waktu_sekarang(a, tz).date().isoformat(), "2026-09-24")  # 23.59 WIB
        a = laporan.buat_parser().parse_args(["--sekarang", "2026-09-24T16:30:00Z"])
        self.assertEqual(laporan.waktu_sekarang(a, laporan.zona("WITA")[0]).date().isoformat(), "2026-09-25")

    def test_periode_mingguan_default_minggu_lalu(self):
        from datetime import date
        a = laporan.buat_parser().parse_args(["--periode", "mingguan"])
        per = laporan.tentukan_periode(a, date(2026, 9, 24))  # Kamis
        self.assertEqual((per["dari"].isoformat(), per["sampai"].isoformat()), ("2026-09-14", "2026-09-20"))
        self.assertEqual(per["banding"][0][1:], (date(2026, 9, 7), date(2026, 9, 13)))
        per = laporan.tentukan_periode(a, date(2026, 9, 28))  # Senin pagi -> minggu 21-27
        self.assertEqual((per["dari"].isoformat(), per["sampai"].isoformat()), ("2026-09-21", "2026-09-27"))

    def test_periode_minggu_berjalan_dipotong_hari_ini(self):
        from datetime import date
        a = laporan.buat_parser().parse_args(["--periode", "mingguan", "--tanggal", "2026-09-24"])
        per = laporan.tentukan_periode(a, date(2026, 9, 24))
        self.assertEqual(per["sampai"].isoformat(), "2026-09-24")
        self.assertTrue(per["berjalan"])
        self.assertEqual(per["banding"][0][1:], (date(2026, 9, 14), date(2026, 9, 17)))


# ------------------------------------------------------------------ uji dengan alat asli
@unittest.skipUnless(SEMUA_ALAT,
                     "alat kasir-lokal/buku-stok/absensi-lokal/pengingat-follow-up/crm-wa tidak ada di folder skills")
class UjiGabungan(Dasar):
    def test_semua_alat_harian_angka_dari_kasir(self):
        akar = self.salin("semua")
        d = self.jalan(akar, "--json")
        kas = alat(KASIR, "rekap", "--tanggal", "2026-09-24", "--json", data=akar / "data")
        pj = d["penjualan"]
        self.assertEqual(pj["omzet"], kas["penjualan_bersih"])
        self.assertEqual(pj["omzet"], 69000)
        self.assertEqual(pj["per_metode"], {"Tunai": 51000, "QRIS": 18000})
        self.assertEqual(pj["nota_sah"], 2)
        # verifikasi independen: 69.000 / 2 = 34.500
        self.assertEqual(pj["rata_rata_per_nota"], 34500)
        self.assertEqual(pj["terlaris"][0]["nama"], "Kopi Susu Gula Aren")
        for n in ("kasir", "stok", "absensi", "pengingat", "crm"):
            self.assertEqual(d["alat"][n]["status"], "ada", d["alat"][n])

    def test_perbandingan_persen_kemarin_dan_minggu_lalu(self):
        d = self.jalan(self.salin("banding"), "--json")
        b = d["penjualan"]["banding"]
        self.assertEqual(b["kemarin"]["omzet"], 36000)
        self.assertEqual(b["minggu_lalu"]["omzet"], 12000)
        # (69000-36000)/36000*100 = 91,666.. -> 91,7 ; (69000-12000)/12000*100 = 475,0
        harap = (Decimal(33000) * 100 / Decimal(36000)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        self.assertEqual(b["kemarin"]["persen"], str(harap))
        self.assertEqual(b["kemarin"]["teks"], "naik 91,7%")
        self.assertEqual(b["minggu_lalu"]["teks"], "naik 475,0%")

    def test_pembanding_nol_tidak_dibagi(self):
        d = self.jalan(self.salin("nol"), "--json", "--tanggal", "2026-09-17")
        b = d["penjualan"]["banding"]
        self.assertEqual(b["kemarin"]["omzet"], 0)
        self.assertIsNone(b["kemarin"]["persen"])
        self.assertIn("persen tidak dihitung", b["kemarin"]["teks"])

    def test_perhatian_selisih_kas_void_dan_belum_impor(self):
        teks = self.jalan(self.salin("perhatian"))
        self.assertIn("KURANG Rp 11.000", teks)
        self.assertIn("1 void", teks)
        self.assertIn("2026-09-24 belum diimpor ke buku-stok", teks)
        self.assertNotIn("2026-09-23 belum diimpor", teks)

    def test_stok_minus_habis_menipis(self):
        d = self.jalan(self.salin("stok"), "--json")
        st = d["stok"]
        self.assertEqual([p["sku"] for p in st["minus"]], ["RB"])
        self.assertEqual([p["sku"] for p in st["habis"]], ["ETM"])
        self.assertEqual([p["sku"] for p in st["menipis"]], ["KH"])
        self.assertTrue(any("MINUS" in s for s in d["perhatian"]))

    def test_kehadiran_harian(self):
        d = self.jalan(self.salin("hadir"), "--json")
        h = d["kehadiran"]
        self.assertEqual(h["terjadwal"], 5)
        self.assertEqual(sorted(h["hadir"]), ["Andi", "Sari"])
        self.assertEqual(h["terlambat"], [{"nama": "Andi", "jam": "08.12", "menit": 12}])
        self.assertEqual(h["izin_sakit_cuti_dinas"], [{"nama": "Budi", "jenis": "sakit"}])
        self.assertEqual(h["alpa"], ["Rina"])
        self.assertEqual(h["tanpa_keterangan"], ["Joko"])
        self.assertEqual(h["lembur_disetujui"], [{"nama": "Andi", "jam": "1"}])
        self.assertEqual([x["nama"] for x in h["lembur_perlu_keputusan"]], ["Sari"])

    def test_samarkan_nama_karyawan(self):
        teks = self.jalan(self.salin("samar"), "--samarkan")
        for nama in ("Andi", "Sari", "Budi", "Rina", "Joko"):
            self.assertNotIn(nama, teks)
        self.assertIn("A. 08.12", teks)

    def test_tanpa_nama_pelanggan_pengingat(self):
        akar = self.salin("privasi")
        teks = self.jalan(akar, "--tanggal", "2026-09-24")
        d = self.jalan(akar, "--json")
        for rahasia in ("CV Contoh Maju", "Bu Rina", "Pak Budi", "INV-0788", "pencairan proyek", "Bu Maya"):
            self.assertNotIn(rahasia, teks)
            self.assertNotIn(rahasia, json.dumps(d, ensure_ascii=False))
        self.assertEqual(d["tagihan"]["total_tertunggak"], 12500000)
        self.assertEqual([x["id"] for x in d["tagihan"]["terlambat"]], ["2"])

    def test_hanya_baca_file_asli_tidak_berubah(self):
        akar = self.salin("hanyabaca")
        sebelum = md5_folder(akar / "data")
        sebelum_csv = md5_folder(akar / "kerja")
        self.jalan(akar)
        self.jalan(akar, "--periode", "mingguan", "--tanggal", "2026-09-24")
        self.assertEqual(md5_folder(akar / "data"), sebelum)  # tidak ada file baru/berubah (termasuk -journal)
        self.assertEqual(md5_folder(akar / "kerja"), sebelum_csv)

    def test_db_terkunci_tidak_menggantung(self):
        akar = self.salin("kunci")
        con = sqlite3.connect(str(akar / "data" / "kasir" / "kasir.db"), isolation_level=None)
        con.execute("BEGIN EXCLUSIVE")
        try:
            d = self.jalan(akar, "--json", "--timeout", "1")
        finally:
            con.execute("ROLLBACK")
            con.close()
        self.assertEqual(d["alat"]["kasir"]["status"], "gagal")
        self.assertIn("sedang dipakai", d["alat"]["kasir"]["pesan"])
        self.assertIsNone(d["penjualan"])
        self.assertEqual(d["alat"]["absensi"]["status"], "ada")  # alat lain tetap jalan
        self.assertLess(self.durasi, 25)

    def test_db_rusak(self):
        akar = self.salin("rusak")
        (akar / "data" / "absensi" / "absensi.db").write_bytes(b"ini bukan database" * 100)
        d = self.jalan(akar, "--json")
        self.assertEqual(d["alat"]["absensi"]["status"], "gagal")
        self.assertIsNone(d["kehadiran"])
        self.assertIn("Belum ada data", d["teks"].split("KEHADIRAN")[1])

    def test_hanya_kasir(self):
        akar = self.salin("hanyakasir")
        os.remove(str(akar / "data" / "stok.db"))
        shutil.rmtree(str(akar / "data" / "absensi"))
        shutil.rmtree(str(akar / "kerja" / "pengingat"))
        d = self.jalan(akar, "--json")
        self.assertEqual(d["penjualan"]["omzet"], 69000)
        self.assertIsNone(d["stok"])
        self.assertEqual(d["alat"]["stok"]["status"], "tidak_ada")
        self.assertIn("Belum ada data (buku-stok belum dipakai", d["teks"])
        self.assertIn("Belum ada data (pengingat-follow-up belum dipakai", d["teks"])
        self.assertFalse(any("belum diimpor ke buku-stok" in s for s in d["perhatian"]))

    def test_tanpa_kasir_penjualan_dari_buku_stok(self):
        akar = self.salin("hanyastok")
        shutil.rmtree(str(akar / "data" / "kasir"))
        d = self.jalan(akar, "--json")
        ring = alat(STOK, "laporan", "ringkas", "--tanggal", "2026-09-24", "--json", data=akar / "data")
        self.assertEqual(d["penjualan"]["sumber"], "buku-stok")
        self.assertEqual(d["penjualan"]["omzet"], ring["omzet_tercatat"])
        self.assertIn("PENJUALAN (dari buku-stok)", d["teks"])

    def test_data_kosong(self):
        akar = self.kosong("datakosong")
        data = akar / "data"
        alat(KASIR, "init", "--nama-toko", "Toko Baru", "--ya", "--json", data=data)
        alat(ABSENSI, "init", "--ya", "--json", data=data)
        alat(STOK, "init", "--ya", "--json", data=data)
        d = self.jalan(akar, "--json")
        self.assertIn("Belum ada transaksi tercatat di kasir.", d["teks"])
        self.assertIsNone(d["penjualan"]["rata_rata_per_nota"])
        self.assertEqual(d["kehadiran"]["terjadwal"], 0)
        self.assertIn("Semua stok di atas batas minimum.", d["teks"])

    def test_tidak_ada_alat_sama_sekali(self):
        akar = self.kosong("nihil")
        teks = self.jalan(akar)
        self.assertEqual(teks.count("Belum ada data ("), 5)  # + PROSPEK (crm-wa)
        self.assertIn("Belum ada data dari alat mana pun", teks)

    def test_script_alat_tidak_ditemukan(self):
        akar = self.salin("tanpascript")
        d = self.jalan(akar, "--json", "--kasir-script", str(akar / "tidak-ada.py"))
        self.assertEqual(d["alat"]["kasir"]["status"], "gagal")
        self.assertIn("script kasir.py tidak ditemukan", d["alat"]["kasir"]["pesan"])

    def test_mingguan(self):
        d = self.jalan(self.salin("mingguan"), "--json", "--periode", "mingguan", "--tanggal", "2026-09-24")
        self.assertEqual(d["periode"]["dari"], "2026-09-21")
        self.assertEqual(d["periode"]["sampai"], "2026-09-24")
        self.assertTrue(d["periode"]["minggu_berjalan"])
        # 21-24 Sep: 36.000 + 69.000 ; pembanding 14-17 Sep: 12.000
        self.assertEqual(d["penjualan"]["omzet"], 105000)
        self.assertEqual(d["penjualan"]["banding"]["minggu_sebelumnya"]["omzet"], 12000)
        self.assertEqual(d["penjualan"]["banding"]["minggu_sebelumnya"]["teks"], "naik 775,0%")
        self.assertEqual(d["kehadiran"]["jenis"], "mingguan")
        self.assertEqual(d["kehadiran"]["alpa"], 1)
        self.assertIn("LAPORAN MINGGUAN USAHA", d["teks"])

    def test_tengah_malam_wib_pindah_tanggal(self):
        # 17.30 UTC = 00.30 WIB tanggal 25: laporan untuk tanggal 25 (belum ada transaksi)
        d = self.jalan(self.salin("malam"), "--json", "--sekarang", "2026-09-24T17:30:00Z")
        self.assertEqual(d["periode"]["dari"], "2026-09-25")
        self.assertEqual(d["penjualan"]["omzet"], 0)
        self.assertEqual(d["penjualan"]["banding"]["kemarin"]["omzet"], 69000)
        self.assertEqual(d["penjualan"]["banding"]["kemarin"]["teks"], "turun 100,0%")

    def test_teks_sama_dengan_json(self):
        akar = self.salin("teksjson")
        d = self.jalan(akar, "--json")
        teks = self.jalan(akar)
        self.assertEqual(teks.strip(), d["teks"].strip())
        self.assertIn("Kamis, 24 September 2026", teks)
        self.assertIn("Dibuat 2026-09-24 21:00 WIB", teks)

    def test_baris_pengingat_rusak_dilaporkan(self):
        akar = self.salin("pengingatrusak")
        f = akar / "kerja" / "pengingat" / "DAFTAR.csv"
        with open(str(f), "a", encoding="utf-8") as fh:
            fh.write("8,piutang,PLG-09,31/02/2026,abc,INV-9,aktif,,2026-09-24,\n")
        d = self.jalan(akar, "--json")
        self.assertEqual(d["tagihan"]["baris_ditolak"], 1)
        self.assertTrue(any("rusak" in s for s in d["perhatian"]))

    def test_env_override_lokasi_db(self):
        akar = self.salin("envdb")
        lain = akar / "lain"
        lain.mkdir()
        shutil.move(str(akar / "data" / "kasir" / "kasir.db"), str(lain / "toko.db"))
        d = self.jalan(akar, "--json", env_tambah={"KOMUNITECH_KASIR_DB": str(lain / "toko.db")})
        self.assertEqual(d["alat"]["kasir"]["status"], "ada")
        self.assertEqual(d["penjualan"]["omzet"], 69000)
        d2 = self.jalan(akar, "--json", "--kasir-db", str(lain / "toko.db"))
        self.assertEqual(d2["penjualan"]["omzet"], 69000)

    def test_jam_komputer_bukan_wib_diperingatkan(self):
        d = self.jalan(self.salin("tzutc"), "--json", tz="UTC")
        self.assertTrue(any("Jam komputer ini bukan Asia/Jakarta" in s for s in d["perhatian"]))
        d = self.jalan(self.salin("tzwib"), "--json", tz="Asia/Jakarta")
        self.assertFalse(any("Jam komputer" in s for s in d["perhatian"]))

    def test_argumen_salah_dan_tanggal_masa_depan(self):
        akar = self.kosong("argsalah")
        out = self.jalan(akar, "--tanpa", "kulkas", harap_kode=2)
        self.assertIn("--tanpa hanya menerima", out)
        out = self.jalan(akar, "--tanggal", "2026-09-30", harap_kode=2)
        self.assertIn("belum terjadi", out)
        out = self.jalan(akar, "--tanggal", "31/02/2026", harap_kode=2)
        self.assertIn("tidak ada di kalender", out)

    def test_tanpa_melewati_alat(self):
        d = self.jalan(self.salin("lewati"), "--json", "--tanpa", "absensi,pengingat")
        self.assertEqual(d["alat"]["absensi"]["status"], "dilewati")
        self.assertIsNone(d["kehadiran"])
        self.assertIsNone(d["tagihan"])
        self.assertIsNotNone(d["penjualan"])

    # ------------------------------------------------------------- S1: impor sebagian kasir -> buku-stok
    def test_impor_sebagian_kasir_ke_stok_terdeteksi(self):
        """S1: impor SEBAGIAN nota kasir tanggal 24/9 (hanya N-260924-0001 dari 2 nota sah) harus terdeteksi
        dengan hitungan benar, dan peringatan hilang begitu semua nota diimpor."""
        akar = self.salin("imporsebagian")
        data = akar / "data"
        penuh = akar / "j24-penuh.csv"
        alat(KASIR, "ekspor", "--format", "buku-stok", "--tanggal", "2026-09-24", "--csv", penuh, "--json", data=data)
        with open(penuh, encoding="utf-8-sig", newline="") as f:
            baris = list(csv.reader(f, delimiter=";"))
        header, isi = baris[0], baris[1:]
        self.assertEqual({r[0] for r in isi}, {"N-260924-0001", "N-260924-0002", "N-260924-0003"})  # 0003 = di-void
        sebagian = akar / "j24-sebagian.csv"
        with open(sebagian, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(header)
            w.writerows(r for r in isi if r[0] == "N-260924-0001")
        alat(STOK, "impor-pesanan", sebagian, "--platform", "lainnya", "--ya", "--json", data=data)
        d = self.jalan(akar, "--json")
        self.assertTrue(any("1 dari 2 nota kasir tanggal 2026-09-24 belum diimpor ke buku-stok (stok belum terpotong)."
                             in s for s in d["perhatian"]), d["perhatian"])
        # lengkapi impor (termasuk baris nota yang di-void, berstatus Dibatalkan) -> peringatan hilang
        alat(STOK, "impor-pesanan", penuh, "--platform", "lainnya", "--ya", "--json", data=data)
        d2 = self.jalan(akar, "--json")
        self.assertFalse(any("belum diimpor ke buku-stok" in s for s in d2["perhatian"]), d2["perhatian"])

    # ------------------------------------------------------------- R1: absen tanpa keterangan hari ini
    def test_tanpa_keterangan_hari_ini_tampil_di_perhatian(self):
        d = self.jalan(self.salin("r1"), "--json")  # SEKARANG = 21:00, setelah jam pulang shift REG (17:00)
        self.assertTrue(any("Joko" in s and "tanpa keterangan" in s for s in d["perhatian"]), d["perhatian"])
        teks = self.jalan(self.salin("r1samar"), "--samarkan")
        self.assertNotIn("Joko", teks)
        self.assertIn("tanpa keterangan", teks)

    # ------------------------------------------------------------- R2: sebelum jadwal mulai, jangan alarm
    def test_belum_waktunya_absen_tidak_memberi_alarm_palsu(self):
        d = self.jalan(self.salin("r2"), "--json", "--sekarang", "2026-09-25T00:30+07:00")
        self.assertTrue(any("Belum waktunya absen (jadwal mulai 08.00)." in s for s in d["perhatian"]), d["perhatian"])
        self.assertFalse(any("Belum ada satu pun data absen" in s for s in d["perhatian"]))

    # ------------------------------------------------------------- R3: zona toko kasir vs --tz laporan
    def test_zona_toko_kasir_beda_dengan_tz_laporan(self):
        akar = self.salin("zonatoko")
        alat(KASIR, "atur", "--zona", "WITA", "--ya", "--json", data=akar / "data")
        d = self.jalan(akar, "--json")  # --tz default Asia/Jakarta, toko WITA
        self.assertTrue(any("Toko diatur zona Asia/Makassar" in s and "--tz Asia/Jakarta" in s
                             for s in d["perhatian"]), d["perhatian"])
        d2 = self.jalan(akar, "--json", "--tz", "Asia/Makassar")
        self.assertFalse(any("Toko diatur zona" in s for s in d2["perhatian"]), d2["perhatian"])

    # ------------------------------------------------------------- R4: pesan error DB rusak pakai path asli
    def test_pesan_db_rusak_pakai_path_asli_bukan_salinan(self):
        akar = self.salin("dbasli")
        asli = akar / "data" / "absensi" / "absensi.db"
        asli.write_bytes(b"")
        d = self.jalan(akar, "--json")
        pesan = d["alat"]["absensi"]["pesan"]
        self.assertIn(str(asli), pesan)  # path file ASLI ada di pesan
        self.assertNotIn(str(Path(tempfile.gettempdir())), pesan.replace(str(asli), ""))  # bukan path salinan

    # ------------------------------------------------------------- kosmetik: --tz di luar Indonesia ditolak
    def test_tz_di_luar_indonesia_ditolak(self):
        akar = self.kosong("tzasing")
        out = self.jalan(akar, "--tz", "Asia/Tokyo", harap_kode=2)
        self.assertIn("di luar Indonesia", out)

    # ------------------------------------------------------------- kosmetik: tanpa minus ganda pada void/retur
    def test_void_retur_tanpa_minus_ganda(self):
        teks = self.jalan(self.salin("kosmetikminus"))  # master: 1 nota di-void (1 kopi hitam, Rp 12.000)
        self.assertNotIn("(-Rp", teks)
        self.assertIn("Retur 0 | void 1 (Rp 12.000)", teks)

    # ------------------------------------------------------------- kosmetik: catatan pajak di per metode bayar
    def test_per_metode_bayar_berlabel_termasuk_pajak(self):
        akar = self.kosong("pajak")
        data = akar / "data"
        alat(KASIR, "init", "--nama-toko", "Toko Pajak", "--stok", "tidak", "--pajak", "ppn-belum", "--pkp", "ya",
             "--ya", "--json", data=data)
        alat(KASIR, "produk", "tambah", "--kode", "A", "--nama", "Barang A", "--harga", "100000", "--ya", "--json",
             data=data)
        alat(KASIR, "jual", "--pesan", "1 barang a, bayar tunai", "--waktu", "2026-09-24 10:00", "--ya", "--json",
             data=data)
        teks = self.jalan(akar, "--tanpa", "stok,absensi,pengingat")
        self.assertIn("Per metode bayar (termasuk pajak/service, omzet di atas belum termasuk):", teks)

    # ------------------------------------------------------------- PROSPEK (crm-wa), alat ke-5
    def test_crm_prospek_cocok_dengan_rekap_langsung(self):
        """Angka PROSPEK harus SAMA PERSIS dengan `crm.py rekap --json` langsung terhadap data yang sama
        (tidak dihitung ulang dengan rumus lain di laporan.py)."""
        akar = self.salin("crmharian")
        d = self.jalan(akar, "--json")
        kr = alat(CRM, "rekap", "--dari", "2026-09-24", "--sampai", "2026-09-24", "--hari-ini", "2026-09-24",
                  "--json", data=akar / "data")
        pr = d["prospek"]
        self.assertEqual(d["alat"]["crm"]["status"], "ada")
        self.assertEqual(pr["lead_masuk"], kr["periode_ini"]["lead_masuk"])
        self.assertEqual(pr["deal"]["jumlah"], kr["periode_ini"]["deal_baru"]["jumlah"])
        self.assertEqual(pr["deal"]["nilai"], kr["periode_ini"]["deal_baru"]["nilai"])
        self.assertEqual(pr["konversi_teks"], kr["periode_ini"]["konversi_teks"])
        self.assertEqual(pr["kohort"], kr["periode_ini"]["kohort"])
        for f in ("terlambat", "hari_ini", "besok", "order_perlu_konfirmasi", "nilai_terlambat_dan_hari_ini"):
            self.assertEqual(pr["followup"][f], kr["followup"][f], f)
        self.assertEqual(pr["sumber_terbaik"], kr["sumber_terbaik"])
        # verifikasi independen dari data uji (lihat buat_data): 24/9 hanya Mbak Dewi masuk; Bu Sari Toko deal
        # (nilai Rp 6 jt) di tanggal 24/9; follow-up: Bu Rina terlambat, Pak Budi & Mbak Dewi hari ini.
        self.assertEqual(pr["lead_masuk"], 1)
        self.assertEqual(pr["deal"]["jumlah"], 1)
        self.assertEqual(pr["deal"]["nilai"], 6000000)
        self.assertEqual(pr["followup"]["terlambat"], 1)
        self.assertEqual(pr["followup"]["hari_ini"], 2)
        self.assertEqual(pr["followup"]["nilai_terlambat_dan_hari_ini"], 4500000)
        self.assertIn("Prospek baru: 1", d["teks"])
        self.assertIn("Follow-up terlambat 1 | hari ini 2 | besok 0 | order perlu konfirmasi 0", d["teks"])
        self.assertIn("Deal periode ini: 1 senilai Rp 6.000.000 (termasuk dari prospek lama)", d["teks"])

    def test_crm_mingguan_banding_minggu_sebelumnya(self):
        akar = self.salin("crmmingguan")
        d = self.jalan(akar, "--json", "--periode", "mingguan", "--tanggal", "2026-09-20")
        kr = alat(CRM, "rekap", "--dari", "2026-09-14", "--sampai", "2026-09-20", "--hari-ini", "2026-09-24",
                  "--json", data=akar / "data")
        kr_lalu = alat(CRM, "rekap", "--dari", "2026-09-07", "--sampai", "2026-09-13", "--hari-ini", "2026-09-24",
                       "--json", data=akar / "data")
        pr = d["prospek"]
        self.assertEqual(pr["lead_masuk"], kr["periode_ini"]["lead_masuk"])
        self.assertEqual(pr["lead_masuk"], 2)  # Bu Rina (masuk 20/9) + Bu Sari Toko (masuk 18/9)
        self.assertEqual(pr["sumber_terbaik"]["sumber"], "Instagram")
        b = pr["banding"]["minggu_sebelumnya"]
        self.assertEqual(b["lead_masuk"], kr_lalu["periode_ini"]["lead_masuk"])
        self.assertEqual(b["lead_masuk"], 0)
        self.assertIn("vs minggu sebelumnya", d["teks"])

    def test_crm_tidak_terpasang_bukan_error(self):
        akar = self.salin("crmtidakada")
        shutil.rmtree(str(akar / "data" / "crm"))
        d = self.jalan(akar, "--json")
        self.assertEqual(d["alat"]["crm"]["status"], "tidak_ada")
        self.assertIsNone(d["prospek"])
        self.assertIn("Belum ada data (crm-wa belum dipakai", d["teks"])

    def test_crm_db_rusak_dilewati_dengan_catatan(self):
        akar = self.salin("crmrusak")
        (akar / "data" / "crm" / "crm.db").write_bytes(b"bukan database crm" * 20)
        d = self.jalan(akar, "--json")
        self.assertEqual(d["alat"]["crm"]["status"], "gagal")
        self.assertIsNone(d["prospek"])
        self.assertIn("Belum ada data", d["teks"].split("PROSPEK")[1])
        self.assertTrue(any("crm-wa tidak terbaca" in s for s in d["perhatian"]), d["perhatian"])

    def test_crm_script_tidak_ditemukan(self):
        akar = self.salin("crmtanpascript")
        d = self.jalan(akar, "--json", "--crm-script", str(akar / "tidak-ada.py"))
        self.assertEqual(d["alat"]["crm"]["status"], "gagal")
        self.assertIn("script crm.py tidak ditemukan", d["alat"]["crm"]["pesan"])

    def test_tanpa_crm(self):
        d = self.jalan(self.salin("crmlewati"), "--json", "--tanpa", "crm")
        self.assertEqual(d["alat"]["crm"]["status"], "dilewati")
        self.assertIsNone(d["prospek"])

    def test_crm_tanpa_nama_nomor_prospek(self):
        """Privasi: teks & JSON tidak pernah memuat nama/nomor WA prospek (kontrak `rekap --json` crm-wa
        sudah tanpa itu; ini menjaga laporan.py tidak menambahkannya sendiri)."""
        akar = self.salin("crmprivasi")
        teks = self.jalan(akar)
        d = self.jalan(akar, "--json")
        dump = json.dumps(d, ensure_ascii=False)
        for rahasia in ("Bu Rina", "Pak Budi", "Bu Sari Toko", "Mbak Dewi", "Mas Andi",
                        "0812-3000-0001", "0812-3000-0002", "0812-3000-0003", "0812-3000-0005", "0812-3000-0006",
                        "62812", "K0001", "K0002", "K0003", "K0004", "K0005"):
            self.assertNotIn(rahasia, teks)
            self.assertNotIn(rahasia, dump)

    def test_crm_db_asli_tidak_berubah(self):
        """File DB crm-wa asli tidak pernah ditulis (dibuka hanya lewat salinan read-only), sama seperti alat lain."""
        akar = self.salin("crmhash")
        dbfile = akar / "data" / "crm" / "crm.db"
        sebelum = hashlib.md5(dbfile.read_bytes()).hexdigest()
        self.jalan(akar, "--json")
        self.jalan(akar, "--json", "--periode", "mingguan")
        self.assertEqual(hashlib.md5(dbfile.read_bytes()).hexdigest(), sebelum)

    # ------------------------------------------------------------- v1.1.1: perbaikan temuan sisa
    def test_n1_sebagian_tap_sebelum_jam_masuk_tanpa_alarm(self):
        """N1: satu karyawan tap 07.45 (shift 08.00), laporan 07.50 -> tidak ada alarm "belum absen tanpa
        keterangan". Setelah jam masuk (09.00) alarm tetap muncul (perilaku R1 tidak hilang)."""
        akar = self.salin("n1")
        alat(ABSENSI, "catat", "--karyawan", "Sari", "--tanggal", "2026-09-25", "--masuk", "07.45", "--json",
             "--sekarang", "2026-09-25T07:46", "--ya", data=akar / "data")
        d = self.jalan(akar, "--json", "--sekarang", "2026-09-25T07:50+07:00")
        self.assertFalse(any("tanpa keterangan" in s or "Belum ada satu pun" in s or "Belum waktunya" in s
                             for s in d["perhatian"]), d["perhatian"])
        self.assertIn("Belum absen (4)", d["teks"])  # daftar di KEHADIRAN tetap ada, hanya bukan alarm
        d2 = self.jalan(akar, "--json", "--sekarang", "2026-09-25T09:00+07:00")
        self.assertTrue(any("Belum absen tanpa keterangan (4)" in s for s in d2["perhatian"]), d2["perhatian"])

    def test_n2_cek_dilewati_tampil_di_teks(self):
        """N2: cek impor yang dilewati karena struktur tabel berubah juga tampil di teks (sekali), bukan hanya
        di JSON catatan."""
        akar = self.salin("n2")
        con = sqlite3.connect(str(akar / "data" / "stok.db"))
        con.execute("ALTER TABLE pesanan RENAME COLUMN no_pesanan TO no_psn")
        con.commit()
        con.close()
        d = self.jalan(akar, "--json")
        pesan = "Cek impor kasir ke buku-stok dilewati: struktur tabel pesanan berubah."
        self.assertEqual(d["catatan"], [pesan])
        self.assertEqual(d["teks"].count(pesan), 1, d["teks"])
        self.assertIn(pesan, d["perhatian"])

    def test_n3_void_setelah_impor_diingatkan(self):
        """N3: nota 23/9 sudah diimpor ke buku-stok lalu di-void 24/9 -> diingatkan dengan nomor notanya.
        Nota yang di-void SEBELUM diimpor (N-260924-0003 di data master) tidak diingatkan. Setelah ekspor ulang
        23/9 + impor lagi (stok dikembalikan buku-stok), peringatan hilang."""
        akar = self.salin("n3")
        data = akar / "data"
        d0 = self.jalan(akar, "--json")
        self.assertFalse(any("di-void setelah diimpor" in s for s in d0["perhatian"]), d0["perhatian"])
        alat(KASIR, "void", "--nota", "N-260923-0001", "--alasan", "uji", "--waktu", "2026-09-24 14:00", "--json",
             "--hari-ini", "2026-09-24T21:00", "--ya", data=data)
        d = self.jalan(akar, "--json")
        self.assertIn("1 nota kasir di-void setelah diimpor ke buku-stok, stoknya belum dikembalikan (N-260923-0001). "
                      "Ekspor ulang tanggal nota itu dari kasir lalu impor lagi ke buku-stok.", d["perhatian"])
        self.assertEqual(d["penjualan"]["omzet"], d0["penjualan"]["omzet"] - 36000)  # angka kasir tidak diubah laporan
        ulang = akar / "j23-ulang.csv"
        alat(KASIR, "ekspor", "--format", "buku-stok", "--tanggal", "2026-09-23", "--csv", ulang, "--json", data=data)
        alat(STOK, "impor-pesanan", ulang, "--platform", "lainnya", "--ya", "--json", data=data)
        d2 = self.jalan(akar, "--json")
        self.assertFalse(any("di-void setelah diimpor" in s for s in d2["perhatian"]), d2["perhatian"])

    def test_n5_samarkan_tanpa_titik_ganda(self):
        teks = self.jalan(self.salin("n5"), "--samarkan")
        self.assertNotIn("..", teks.split("PERLU PERHATIAN")[1])
        self.assertIn("Belum absen tanpa keterangan (1): J. Tanyakan & catat izin/alpa.", teks)
        teks2 = self.jalan(self.salin("n5b"))
        self.assertIn("Belum absen tanpa keterangan (1): Joko. Tanyakan & catat izin/alpa.", teks2)

    def test_crm_samarkan_diteruskan_angka_sama(self):
        """N-baru: --samarkan diteruskan ke `crm.py rekap`; angka PROSPEK tetap identik."""
        akar = self.salin("crmsamar")
        biasa = self.jalan(akar, "--json")["prospek"]
        samar = self.jalan(akar, "--json", "--samarkan")["prospek"]
        self.assertEqual(biasa, samar)
        dipanggil = []
        asli = laporan.jalankan
        laporan.jalankan = lambda script, argv, timeout: dipanggil.append(argv) or {}
        try:
            per = laporan.tentukan_periode(type("A", (), {"periode": "harian", "tanggal": None})(),
                                           laporan.date(2026, 9, 24))
            for sam in (False, True):
                ctx = {"alat": {"crm": {"script_path": CRM, "snap": "x.db"}}, "periode": per,
                       "hari_ini": laporan.date(2026, 9, 24), "timeout": 1, "samarkan": sam}
                laporan.ambil_crm(ctx)
        finally:
            laporan.jalankan = asli
        self.assertNotIn("--samarkan", dipanggil[0])
        self.assertIn("--samarkan", dipanggil[1])

    def test_order_perlu_konfirmasi_di_perhatian(self):
        """Kosmetik v1.1.0: order (deal) yang jadwal konfirmasinya hari ini/lewat juga jadi butir PERLU PERHATIAN."""
        akar = self.salin("crmorder")
        d0 = self.jalan(akar, "--json")
        self.assertEqual(d0["prospek"]["followup"]["order_perlu_konfirmasi"], 0)
        self.assertFalse(any("order (deal)" in s for s in d0["perhatian"]))
        alat(CRM, "catat", "--kontak", "Mas Andi", "--followup", "2026-09-24", "--json", "--hari-ini", "2026-09-24",
             data=akar / "data")
        d = self.jalan(akar, "--json")
        self.assertEqual(d["prospek"]["followup"]["order_perlu_konfirmasi"], 1)
        self.assertIn("1 order (deal) sudah waktunya dikonfirmasi ke pelanggan. Ketik 'follow-up hari ini' untuk "
                      "daftar & draf pesannya.", d["perhatian"])


def tearDownModule():
    if Dasar.master is not None:
        shutil.rmtree(str(Dasar.master.parent), ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
