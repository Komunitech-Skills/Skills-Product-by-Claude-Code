#!/usr/bin/env python3
"""Uji regresi laporan-harian-usaha.

Data contoh DIBUAT dengan menjalankan script alat asli (kasir-lokal, buku-stok, absensi-lokal,
pengingat-follow-up) di folder sementara, bukan meniru skema dengan tangan. Alat dicari di folder
skills yang sama (../kasir-lokal, dst.); jika tidak ada, uji yang membutuhkannya dilewati.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
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
SEMUA_ALAT = all(p.is_file() for p in (KASIR, STOK, ABSENSI, PENGINGAT, DAFTAR_CONTOH))
SEKARANG = "2026-09-24T21:00:00+07:00"

sys.path.insert(0, str(SINI / "scripts"))
import laporan  # noqa: E402


def alat(script, *argv, data=None):
    env = dict(os.environ)
    env["KOMUNITECH_DATA"] = str(data)
    env.pop("KOMUNITECH_KASIR_DB", None)
    env.pop("KOMUNITECH_STOK_DB", None)
    env.pop("KOMUNITECH_ABSENSI_DB", None)
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
@unittest.skipUnless(SEMUA_ALAT, "alat kasir-lokal/buku-stok/absensi-lokal/pengingat-follow-up tidak ada di folder skills")
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
        for n in ("kasir", "stok", "absensi", "pengingat"):
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
        self.assertEqual(teks.count("Belum ada data ("), 4)
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


def tearDownModule():
    if Dasar.master is not None:
        shutil.rmtree(str(Dasar.master.parent), ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
