#!/usr/bin/env python3
"""Uji regresi resi-picking.

Menjalankan script asli (scripts/resi.py) sebagai subprocess, seperti agent memakainya, lalu
memeriksa JSON keluarannya. Mencakup skenario normal, file rusak, kolom tertukar/tidak umum, dan
baris ringkasan/total di ekspor.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
RESI = SINI / "scripts" / "resi.py"


def jalankan(*argv, cwd):
    p = subprocess.run([sys.executable, str(RESI)] + [str(a) for a in argv],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=str(cwd))
    stdout = p.stdout.decode("utf-8", errors="replace")
    data = json.loads(stdout) if stdout.strip().startswith("{") else None
    return p.returncode, data, stdout, p.stderr.decode("utf-8", errors="replace")


def tulis(dir_, nama, isi):
    path = Path(dir_) / nama
    path.write_text(isi, encoding="utf-8")
    return path


PESANAN_NORMAL = """No. Pesanan,Nomor Referensi SKU,Nama Produk,Nama Variasi,Jumlah,Opsi Pengiriman,No. Resi,Catatan dari Pembeli,Status Pesanan
240901A1,KAOS-HT-M,Kaos Polos Pria,Hitam - M,2,JNE,JX00112233,,Perlu Dikirim
240901A1,TOPI-01,Topi Bucket,Krem,1,JNE,JX00112233,Tolong dibungkus rapi ya kak,Perlu Dikirim
240901A2,KAOS-HT-L,Kaos Polos Pria,Hitam - L,3,SiCepat,SC5566778,,Perlu Dikirim
240901A3,KAOS-HT-M,Kaos Polos Pria,Hitam - M,1,JNE,,,Perlu Dikirim
240901A4,GANTUNGAN-X,Gantungan Kunci Lucu,,5,J&T,JT9988776,,Perlu Dikirim
240901A5,KAOS-HT-M,Kaos Polos Pria,Hitam - M,2,JNE,JX00112299,,Dibatalkan
240901A6,TOPI-01,Topi Bucket,Krem,0,JNE,JX00112300,,Perlu Dikirim
240901A7,,,,-,JNE,JX00112301,,Perlu Dikirim
240901A1,KAOS-HT-M,Kaos Polos Pria,Hitam - M,2,JNE,JX00112233,,Perlu Dikirim
,,Total,,16,,,,
"""

LOKASI = """SKU,Lokasi
KAOS-HT-M,A1
KAOS-HT-L,A2
TOPI-01,B3
"""

STOK_BUKU_STOK = """lokasi,sku,nama,varian,satuan,stok,stok_min,hpp_rata2,nilai_persediaan,harga_jual,status
A1,KAOS-HT-M,Kaos Polos Pria,Hitam - M,pcs,3,10,35000,105000,59000,menipis
A2,KAOS-HT-L,Kaos Polos Pria,Hitam - L,pcs,20,10,35000,700000,59000,aman
B3,TOPI-01,Topi Bucket,Krem,pcs,10,5,20000,200000,45000,aman
"""


class UjiNormal(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.pesanan = tulis(self.dir, "pesanan.csv", PESANAN_NORMAL)
        self.lokasi = tulis(self.dir, "lokasi.csv", LOKASI)
        self.stok = tulis(self.dir, "stok.csv", STOK_BUKU_STOK)

    def tearDown(self):
        self.tmp.cleanup()

    def test_picking_dasar(self):
        kode, data, _, err = jalankan(self.pesanan, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertTrue(data["ok"] is not False)
        # 4 pesanan aktif (A1-A4); A5 batal, A6 qty 0, A7 tanpa data, baris "Total" diabaikan.
        self.assertEqual(data["jumlah_pesanan_aktif"], 4)
        self.assertEqual(data["jumlah_sku_unik"], 4)
        self.assertEqual(data["total_barang"], 12.0)
        self.assertEqual(data["baris_dilewati"].get("baris_ringkasan_diabaikan"), 1)
        self.assertEqual(data["baris_dilewati"].get("baris_duplikat"), 1)
        self.assertEqual(data["baris_dilewati"].get("jumlah_nol_atau_negatif"), 1)
        self.assertEqual(data["baris_dilewati"].get("jumlah_tidak_terbaca"), 1)
        self.assertEqual(data["dilewati_status"].get("batal"), 1)
        self.assertEqual(data["jumlah_resi_kosong"], 1)
        self.assertEqual(data["jumlah_pesanan_catatan_khusus"], 1)
        # Verifikasi angka per SKU secara independen (bukan dari script).
        per_sku = {a["sku"]: a["qty"] for a in data["daftar_ambil"]}
        self.assertEqual(per_sku["KAOS-HT-M"], 3.0)   # A1 (2) + A3 (1)
        self.assertEqual(per_sku["KAOS-HT-L"], 3.0)   # A2
        self.assertEqual(per_sku["TOPI-01"], 1.0)     # A1
        self.assertEqual(per_sku["GANTUNGAN-X"], 5.0)  # A4
        # 3 file keluaran markdown dibuat
        self.assertTrue(Path(data["file_keluaran"]["daftar_ambil_md"]).is_file())
        self.assertTrue(Path(data["file_keluaran"]["urutan_resi_md"]).is_file())
        isi = Path(data["file_keluaran"]["daftar_ambil_md"]).read_text(encoding="utf-8")
        self.assertIn("KAOS-HT-M", isi)
        self.assertIn("Peringatan", isi)

    def test_dengan_lokasi_dan_stok(self):
        kode, data, _, err = jalankan(self.pesanan, "--lokasi", self.lokasi, "--stok", self.stok,
                                      "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        per_sku = {a["sku"]: a for a in data["daftar_ambil"]}
        self.assertEqual(per_sku["KAOS-HT-M"]["lokasi"], "A1")
        self.assertEqual(per_sku["KAOS-HT-L"]["lokasi"], "A2")
        self.assertEqual(per_sku["TOPI-01"]["lokasi"], "B3")
        self.assertEqual(per_sku["GANTUNGAN-X"]["lokasi"], "")
        self.assertFalse(per_sku["GANTUNGAN-X"]["sku_dikenal"])
        # Stok KAOS-HT-M tercatat 3, dibutuhkan 3 -> pas, bukan kurang.
        self.assertTrue(any("GANTUNGAN-X" in p for p in data["peringatan"]))

    def test_stok_kurang_terdeteksi(self):
        stok_kurang = STOK_BUKU_STOK.replace(
            "A1,KAOS-HT-M,Kaos Polos Pria,Hitam - M,pcs,3,10,35000,105000,59000,menipis",
            "A1,KAOS-HT-M,Kaos Polos Pria,Hitam - M,pcs,1,10,35000,35000,59000,menipis")
        stok = tulis(self.dir, "stok-kurang.csv", stok_kurang)
        kode, data, _, err = jalankan(self.pesanan, "--stok", stok, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertTrue(any("kemungkinan kurang" in p and "KAOS-HT-M" in p for p in data["peringatan"]))

    def test_dilewati_rinci_menyebut_nomor_pesanan(self):
        # v1.0.5: pesanan/baris yang tidak diproses harus disebut nomornya, bukan hanya jumlahnya.
        kode, data, _, err = jalankan(self.pesanan, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["jumlah_pesanan_di_file"], 7)            # A1..A7
        self.assertEqual(data["jumlah_pesanan_aktif"], 4)              # A1..A4
        self.assertEqual(data["jumlah_pesanan_data_bermasalah"], 2)    # A6, A7
        self.assertEqual(data["dilewati_status"], {"batal": 1})        # A5
        # 7 = 4 aktif + 1 batal + 2 data bermasalah
        self.assertEqual(data["jumlah_pesanan_di_file"],
                         data["jumlah_pesanan_aktif"] + sum(data["dilewati_status"].values())
                         + data["jumlah_pesanan_data_bermasalah"])
        alasan = {e["no_pesanan"]: e["alasan"] for e in data["dilewati_rinci"] if e["no_pesanan"]}
        self.assertEqual(alasan["240901A5"], "batal")
        self.assertIn("0", alasan["240901A6"])
        self.assertIn("tidak terbaca", alasan["240901A7"])
        # Jumlah rincian = jumlah semua baris yang dilewati + 1 pesanan batal.
        self.assertEqual(len(data["dilewati_rinci"]), sum(data["baris_dilewati"].values()) + 1)
        # Urut menurut nomor baris di file.
        urut = [e["baris"][0] for e in data["dilewati_rinci"]]
        self.assertEqual(urut, sorted(urut))

    def test_pesanan_aktif_dengan_satu_baris_dilewati_tetap_tercatat(self):
        isi = ("No. Pesanan,SKU,Nama Produk,Jumlah,Status Pesanan\n"
               "X1,SKU-A,Barang A,2,Perlu Dikirim\n"
               "X1,SKU-B,Barang B,0,Perlu Dikirim\n"
               "X2,SKU-A,Barang A,1,Belum Bayar\n")
        f = tulis(self.dir, "pesanan-x.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["jumlah_pesanan_di_file"], 2)
        self.assertEqual(data["jumlah_pesanan_aktif"], 1)
        self.assertEqual(data["jumlah_pesanan_data_bermasalah"], 0)
        self.assertEqual(data["dilewati_status"], {"belum bayar": 1})
        pasangan = {(e["no_pesanan"], e["alasan"]) for e in data["dilewati_rinci"]}
        self.assertIn(("X1", "jumlah 0 atau negatif"), pasangan)   # baris item X1 yang hilang tetap disebut
        self.assertIn(("X2", "belum bayar"), pasangan)

    def test_nomor_pesanan_rusak_excel_disebut_apa_adanya(self):
        isi = ("No. Pesanan,SKU,Nama Produk,Jumlah\n"
               "R1,SKU-A,Barang A,1\n"
               "2.4E+17,SKU-A,Barang A,1\n")
        f = tulis(self.dir, "pesanan-rusak.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        rusak = [e for e in data["dilewati_rinci"] if "rusak" in e["alasan"]]
        self.assertEqual(len(rusak), 1)
        self.assertEqual(rusak[0]["no_pesanan"], "2.4E+17")
        self.assertEqual(data["jumlah_pesanan_di_file"], 1)

    def test_stok_setelah_dikemas_menandai_habis_dan_di_bawah_minimum(self):
        kode, data, _, err = jalankan(self.pesanan, "--lokasi", self.lokasi, "--stok", self.stok,
                                      "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        per_sku = {a["sku"]: a for a in data["daftar_ambil"]}
        # Angka dihitung ulang sendiri: stok - qty. KAOS-HT-M 3-3=0 (habis), KAOS-HT-L 20-3=17, TOPI-01 10-1=9.
        self.assertEqual(per_sku["KAOS-HT-M"]["stok_setelah"], 0.0)
        self.assertEqual(per_sku["KAOS-HT-M"]["status_stok_setelah"], "habis")
        self.assertEqual(per_sku["KAOS-HT-M"]["stok_min"], 10.0)
        self.assertEqual(per_sku["KAOS-HT-L"]["stok_setelah"], 17.0)
        self.assertEqual(per_sku["KAOS-HT-L"]["status_stok_setelah"], "aman")
        self.assertEqual(per_sku["TOPI-01"]["stok_setelah"], 9.0)
        self.assertEqual(per_sku["TOPI-01"]["status_stok_setelah"], "aman")
        self.assertIsNone(per_sku["GANTUNGAN-X"]["stok_setelah"])   # tidak ada di file stok
        # Di bawah minimum tapi belum habis: stok TOPI-01 diubah jadi 5 -> setelah 4 < min 5.
        stok2 = tulis(self.dir, "stok2.csv", STOK_BUKU_STOK.replace(
            "B3,TOPI-01,Topi Bucket,Krem,pcs,10,5,20000,200000,45000,aman",
            "B3,TOPI-01,Topi Bucket,Krem,pcs,5,5,20000,100000,45000,aman"))
        kode, data, _, err = jalankan(self.pesanan, "--stok", stok2, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        topi = {a["sku"]: a for a in data["daftar_ambil"]}["TOPI-01"]
        self.assertEqual(topi["stok_setelah"], 4.0)
        self.assertEqual(topi["status_stok_setelah"], "di bawah minimum")

    def test_stok_tanpa_kolom_minimum_hanya_menandai_habis_atau_kurang(self):
        stok = tulis(self.dir, "stok-polos.csv", "sku,stok\nKAOS-HT-M,2\nKAOS-HT-L,20\nTOPI-01,1\nGANTUNGAN-X,9\n")
        kode, data, _, err = jalankan(self.pesanan, "--stok", stok, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        per_sku = {a["sku"]: a for a in data["daftar_ambil"]}
        self.assertEqual(per_sku["KAOS-HT-M"]["status_stok_setelah"], "kurang")   # 2 - 3 = -1
        self.assertEqual(per_sku["KAOS-HT-L"]["status_stok_setelah"], "aman")     # tanpa minimum
        self.assertEqual(per_sku["TOPI-01"]["status_stok_setelah"], "habis")      # 1 - 1 = 0
        self.assertIsNone(per_sku["TOPI-01"]["stok_min"])

    def test_markdown_memuat_dilewati_dan_stok_setelah_dikemas(self):
        kode, data, _, err = jalankan(self.pesanan, "--lokasi", self.lokasi, "--stok", self.stok,
                                      "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        isi = Path(data["file_keluaran"]["daftar_ambil_md"]).read_text(encoding="utf-8")
        self.assertIn("Pesanan di file: 7", isi)
        self.assertIn("Dilewati:", isi)
        for nomor in ("240901A5", "240901A6", "240901A7"):
            self.assertIn("#" + nomor, isi)
        self.assertIn("## Stok setelah dikemas", isi)
        self.assertIn("KAOS-HT-M", isi.split("## Stok setelah dikemas")[1])
        self.assertIn("HABIS", isi)

    def test_markdown_tanpa_file_stok_tidak_ada_bagian_stok(self):
        kode, data, _, err = jalankan(self.pesanan, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        isi = Path(data["file_keluaran"]["daftar_ambil_md"]).read_text(encoding="utf-8")
        self.assertNotIn("Stok setelah dikemas", isi)
        self.assertIsNone(data["daftar_ambil"][0]["stok_setelah"])

    def test_tidak_ada_yang_dilewati_dilaporkan_tegas(self):
        isi = "No. Pesanan,SKU,Nama Produk,Jumlah\nT1,SKU-A,Barang A,2\n"
        f = tulis(self.dir, "bersih.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["dilewati_rinci"], [])
        self.assertEqual(data["jumlah_pesanan_di_file"], 1)
        md = Path(data["file_keluaran"]["daftar_ambil_md"]).read_text(encoding="utf-8")
        self.assertIn("Dilewati: tidak ada.", md)

    def test_urutan_resi_dikelompokkan_per_kurir(self):
        kode, data, _, err = jalankan(self.pesanan, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(sorted(data["kurir"].keys()), sorted(["JNE", "SiCepat", "J&T"]))
        self.assertEqual(data["kurir"]["JNE"], 2)   # A1 & A3
        self.assertEqual(data["kurir"]["SiCepat"], 1)
        self.assertEqual(data["kurir"]["J&T"], 1)

    def test_html_dan_csv_opsional(self):
        kode, data, _, err = jalankan(self.pesanan, "--html", "--csv", "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        for k in ("daftar_ambil_html", "urutan_resi_html", "daftar_ambil_csv", "urutan_resi_csv"):
            self.assertTrue(Path(data["file_keluaran"][k]).is_file(), k)

    def test_teks_biasa_tanpa_json(self):
        kode, data, stdout, err = jalankan(self.pesanan, cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertIn("Daftar Ambil Barang", stdout)
        self.assertIn("Urutan Kemas", stdout)


class UjiInputBuruk(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_file_tidak_ada(self):
        kode, data, _, _ = jalankan(self.dir / "tidak-ada.csv", "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertFalse(data["ok"])
        self.assertIn("tidak ditemukan", data["error"])

    def test_file_kosong(self):
        f = tulis(self.dir, "kosong.csv", "")
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("kosong", data["error"])

    def test_file_xlsx_asli_ditolak_dengan_jelas(self):
        f = self.dir / "pesanan.xlsx"
        with zipfile.ZipFile(f, "w") as z:
            z.writestr("a.txt", "x")
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("Excel", data["error"])

    def test_file_biner_bernama_csv_ditolak(self):
        f = self.dir / "pesanan.csv"
        with zipfile.ZipFile(f, "w") as z:
            z.writestr("a.txt", "x")
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("Excel", data["error"])

    def test_csv_rusak_pemisah_tidak_konsisten(self):
        f = tulis(self.dir, "rusak.csv", "No. Pesanan,SKU,Nama Produk,Jumlah\n\"A1,B,C\n")
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        # Sniffer mungkin tetap membaca dengan longgar; yang penting tidak crash dan tetap JSON valid.
        self.assertIn(kode, (0, 1))
        self.assertIsNotNone(data)

    def test_kolom_wajib_tidak_ada(self):
        f = tulis(self.dir, "tanpa-qty.csv", "No. Pesanan,SKU,Nama Produk\nX1,ABC,Barang\n")
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("Jumlah", data["error"])

    def test_semua_pesanan_batal(self):
        f = tulis(self.dir, "semua-batal.csv",
                  "No. Pesanan,SKU,Nama Produk,Jumlah,Status Pesanan\nB1,ABC,Barang,2,Dibatalkan\n")
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("batal", data["error"].lower())

    def test_bukan_file_pesanan_di_luar_cakupan(self):
        # File laporan penjualan biasa (bukan ekspor pesanan) -> kolom tidak dikenali, gagal jujur.
        f = tulis(self.dir, "laporan-lain.csv", "Tanggal,Total Omzet\n2026-09-01,150000\n")
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertFalse(data["ok"])


class UjiKolomTertukarDanOverride(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_urutan_kolom_berbeda_tetap_terdeteksi(self):
        # Kolom sengaja disusun terbalik/acak dibanding urutan sinonim internal.
        isi = ("Qty;Variation;Product Name;Seller SKU;Shipping Provider Name;Tracking Number;Order ID\n"
              "4;Merah;Mug Custom;MUG-01;J&T Express;TRK111;9001\n"
              "2;;Stiker Lucu;STIKER-A;J&T Express;TRK111;9001\n"
              "1;Biru;Mug Custom;MUG-01;JNE;TRK222;9002\n")
        f = tulis(self.dir, "pesanan-en.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["jumlah_sku_unik"], 2)
        self.assertEqual(data["total_barang"], 7.0)
        self.assertEqual(data["pemetaan_kolom"]["No. pesanan"], "Order ID")
        self.assertEqual(data["pemetaan_kolom"]["Jumlah"], "Qty")

    def test_nama_kolom_tidak_umum_dengan_override_manual(self):
        isi = "KodePesanan,Barang,Banyak,Ongkir\nZ1,Sabun,3,GoSend\nZ2,Sampo,2,GoSend\n"
        f = tulis(self.dir, "aneh.csv", isi)
        kode, data, _, err = jalankan(
            f, "--kolom-no-pesanan", "KodePesanan", "--kolom-nama", "Barang",
            "--kolom-qty", "Banyak", "--kolom-kurir", "Ongkir", "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["jumlah_sku_unik"], 2)
        self.assertEqual(data["total_barang"], 5.0)

    def test_override_kolom_tidak_ada_gagal_jujur(self):
        f = tulis(self.dir, "pesanan.csv", PESANAN_NORMAL)
        kode, data, _, _ = jalankan(f, "--kolom-sku", "TidakAda", "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("TidakAda", data["error"])

    def test_kolom_diabaikan_dengan_tanda_minus(self):
        f = tulis(self.dir, "pesanan.csv", PESANAN_NORMAL)
        kode, data, _, err = jalankan(f, "--kolom-sku", "-", "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertNotIn("SKU", data["pemetaan_kolom"])
        # Tanpa SKU, barang dikelompokkan lewat nama+varian -> tetap 4 jenis barang.
        self.assertEqual(data["jumlah_sku_unik"], 4)


class UjiHeaderMarketplaceAsli(unittest.TestCase):
    """v1.0.1: header rekaan (data fiktif) meniru pola nama kolom tiap marketplace, supaya
    auto-deteksi kolom (SINONIM_PESANAN / deteksi_kolom) diuji dengan header realistis, bukan cuma
    header rapi buatan sendiri. Lihat examples/HASIL-UJI.md temuan Akun B (deteksi 0/2 pada header
    TikTok Shop & Tokopedia sebelum v1.0.1) dan references/sumber-kolom-marketplace.md untuk status
    verifikasi tiap nama kolom (resmi vs best-effort)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_shopee_header_resmi_id(self):
        isi = ("No. Pesanan,Nomor Referensi SKU,Nama Produk,Nama Variasi,Jumlah,Opsi Pengiriman,"
              "No. Resi,Catatan dari Pembeli,Status Pesanan\n"
              "SP001,SKU-SP-1,Sepatu Lari,42,2,JNE,JX700001,,Perlu Dikirim\n"
              "SP002,SKU-SP-2,Sepatu Lari,43,1,J&T,JX700002,Tolong dibungkus,Perlu Dikirim\n")
        f = tulis(self.dir, "shopee.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["jumlah_pesanan_aktif"], 2)
        self.assertEqual(data["jumlah_sku_unik"], 2)
        self.assertEqual(data["total_barang"], 3.0)
        self.assertEqual(data["pemetaan_kolom"]["Kurir"], "Opsi Pengiriman")

    def test_shopee_header_underscore_kapital_dan_diakritik(self):
        # Underscore, HURUF BESAR semua, dan huruf beraksen (é) - harus tetap terdeteksi.
        isi = ("NO_PESANAN;SKU;NAMA_PRODUK;JUMLAH;KURÍR\n"
              "U1;SKU-U1;Barang Unik;4;JNE\n"
              "U2;SKU-U2;Barang Unik 2;1;J&T\n")
        f = tulis(self.dir, "underscore.csv", isi)
        kode, data, _, err = jalankan(f, "--pemisah", ";", "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["pemetaan_kolom"]["No. pesanan"], "NO_PESANAN")
        self.assertEqual(data["pemetaan_kolom"]["SKU"], "SKU")
        self.assertEqual(data["pemetaan_kolom"]["Kurir"], "KURÍR")
        self.assertEqual(data["total_barang"], 5.0)

    def test_tiktok_shop_header_realistis(self):
        # Header persis seperti temuan Akun B (examples/02-tiktok-tokopedia-gabung.md):
        # "kurir"(5)/"sku"(3) tidak pernah cocok sebagian di v1.0.0 karena aturan lama >= 8 huruf.
        isi = ("Order/adjustment ID;SKU Reference No.;Nama Produk;Nama Variasi;Quantity;"
              "Shipping Provider Name;Tracking ID;Order Substatus;Buyer Message\n"
              "TT-88001;SKU-A;Produk A;Merah;2;JNE;JX88001;Perlu Dikirim;\n"
              "TT-88004;SKU-A;Produk A;Merah;1;JNE;JX88001;Perlu Dikirim;\n"
              "TT-88004;SKU-B;Produk B;;1;JNE;JX88001;Perlu Dikirim;Tolong dibungkus rapi\n"
              "TT-88005;SKU-C;Produk C;Biru;1;SPX Express;JX88002;Perlu Dikirim;\n"
              "TT-88006;SKU-A;Produk A;Merah;2;J&T;JX88003;Dibatalkan;\n")
        f = tulis(self.dir, "tiktok.csv", isi)
        kode, data, _, err = jalankan(f, "--pemisah", ";", "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        # Semua 9 kolom wajib+opsional terdeteksi otomatis TANPA satupun --kolom-... override.
        self.assertEqual(data["pemetaan_kolom"]["No. pesanan"], "Order/adjustment ID")
        self.assertEqual(data["pemetaan_kolom"]["SKU"], "SKU Reference No.")
        self.assertEqual(data["pemetaan_kolom"]["Kurir"], "Shipping Provider Name")
        self.assertEqual(data["pemetaan_kolom"]["No. resi"], "Tracking ID")
        self.assertEqual(data["pemetaan_kolom"]["Status pesanan"], "Order Substatus")
        self.assertEqual(data["pemetaan_kolom"]["Catatan pembeli"], "Buyer Message")
        self.assertEqual(data["jumlah_pesanan_total"], 4)
        self.assertEqual(data["jumlah_pesanan_aktif"], 3)  # TT-88006 batal
        per_sku = {a["sku"]: a["qty"] for a in data["daftar_ambil"]}
        self.assertEqual(per_sku["SKU-A"], 3.0)  # TT-88001 (2) + TT-88004 (1)
        self.assertEqual(per_sku["SKU-B"], 1.0)
        self.assertEqual(per_sku["SKU-C"], 1.0)

    def test_tokopedia_header_realistis(self):
        # Header persis seperti temuan Akun B: "No. Invoice" & "Nama Kurir" tidak cocok di v1.0.0.
        isi = ("No. Invoice,Kode SKU,Nama Barang,Varian,Jumlah Produk Dibeli,Nama Kurir,No Resi,"
              "Status Terakhir,Catatan Pembeli\n"
              "INV-001,SKU-X,Barang X,Hijau,3,SiCepat,SC001,Perlu Dikirim,\n"
              "INV-002,SKU-Y,Barang Y,,1,JNE,JX9001,Perlu Dikirim,Cepat ya kak\n"
              "INV-003,SKU-X,Barang X,Hijau,2,SiCepat,SC002,Retur,\n")
        f = tulis(self.dir, "tokopedia.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["pemetaan_kolom"]["No. pesanan"], "No. Invoice")
        self.assertEqual(data["pemetaan_kolom"]["Nama produk"], "Nama Barang")
        self.assertEqual(data["pemetaan_kolom"]["Kurir"], "Nama Kurir")
        self.assertEqual(data["pemetaan_kolom"]["Status pesanan"], "Status Terakhir")
        self.assertEqual(data["jumlah_pesanan_total"], 3)
        self.assertEqual(data["jumlah_pesanan_aktif"], 2)  # INV-003 retur
        per_sku = {a["sku"]: a["qty"] for a in data["daftar_ambil"]}
        self.assertEqual(per_sku["SKU-X"], 3.0)
        self.assertEqual(per_sku["SKU-Y"], 1.0)

    def test_lazada_header_best_effort(self):
        # Nama kolom Lazada BELUM diverifikasi resmi (lihat references/sumber-kolom-marketplace.md)
        # - dugaan masuk akal dari dokumentasi integrator pihak ketiga.
        isi = ("Order Number,Seller SKU,Item Name,Quantity,Order Item Status,Shipping Provider,Tracking Number\n"
              "LZD-01,SKU-L1,Kemeja Flanel,2,Ready to Ship,Ninja Van,NV0001\n"
              "LZD-02,SKU-L2,Kemeja Flanel,1,Ready to Ship,J&T Express,JT0002\n")
        f = tulis(self.dir, "lazada.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["pemetaan_kolom"]["No. pesanan"], "Order Number")
        self.assertEqual(data["pemetaan_kolom"]["SKU"], "Seller SKU")
        self.assertEqual(data["pemetaan_kolom"]["Nama produk"], "Item Name")
        self.assertEqual(data["pemetaan_kolom"]["Kurir"], "Shipping Provider")
        self.assertEqual(data["pemetaan_kolom"]["No. resi"], "Tracking Number")
        self.assertEqual(data["jumlah_sku_unik"], 2)

    def test_blibli_header_best_effort(self):
        # Nama kolom Blibli BELUM diverifikasi resmi (fetch halaman bantuan tidak mengonfirmasi
        # nama kolom persis) - "Logistik" dimasukkan sebagai dugaan best-effort, ditandai jelas.
        isi = ("No Pesanan,Seller SKU,Nama Produk,Qty,Logistik,No Resi,Status Pesanan\n"
              "BLI-01,SKU-B1,Blender Mini,2,Anteraja,ANT001,Perlu Dikirim\n")
        f = tulis(self.dir, "blibli.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["pemetaan_kolom"]["Kurir"], "Logistik")
        self.assertEqual(data["jumlah_pesanan_aktif"], 1)

    def test_pesan_error_menyertakan_kolom_ditemukan_dan_flag_saran(self):
        # Kolom qty tidak ada sama sekali -> pesan error harus menyebut kolom yang SUDAH
        # terdeteksi otomatis dan flag --kolom-qty persis sebagai saran perbaikan.
        isi = "No. Pesanan,SKU,Nama Produk\nX1,ABC,Barang\n"
        f = tulis(self.dir, "tanpa-qty.csv", isi)
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("--kolom-qty", data["error"])
        self.assertIn("No. pesanan=No. Pesanan", data["error"])

    def test_pesan_error_header_tidak_dikenali_sebutkan_semua_flag(self):
        isi = "KolomAneh1,KolomAneh2\nx,y\n"
        f = tulis(self.dir, "aneh-total.csv", isi)
        kode, data, _, _ = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 1)
        self.assertIn("--kolom-no-pesanan", data["error"])
        self.assertIn("KolomAneh1", data["error"])


class UjiKolomAmbigu(unittest.TestCase):
    """v1.0.2: kalau ada >1 kolom yang sama-sama cocok sinonim suatu field (mis. dua kolom SKU),
    auto-deteksi tetap memilih salah satu (tidak gagal), tapi WAJIB memperingatkan pengguna + saran
    --kolom-... supaya bisa dikoreksi kalau yang dipilih salah."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_dua_kolom_sku_mirip_beri_peringatan_ambigu(self):
        isi = ("No. Pesanan,SKU Induk,Nomor SKU,Nama Produk,Jumlah\n"
              "A1,SKU-INDUK-1,SKU-JUAL-1,Barang A,2\n")
        f = tulis(self.dir, "dua-sku.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertIn("SKU", data["kolom_ambigu"])
        self.assertIn("--kolom-sku", " ".join(data["peringatan"]))

    def test_override_manual_menghilangkan_peringatan_ambigu(self):
        isi = ("No. Pesanan,SKU Induk,Nomor SKU,Nama Produk,Jumlah\n"
              "A1,SKU-INDUK-1,SKU-JUAL-1,Barang A,2\n")
        f = tulis(self.dir, "dua-sku.csv", isi)
        kode, data, _, err = jalankan(f, "--kolom-sku", "Nomor SKU", "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertNotIn("SKU", data["kolom_ambigu"])
        self.assertEqual(data["pemetaan_kolom"]["SKU"], "Nomor SKU")


class UjiBarisRingkasan(unittest.TestCase):
    """Baris total/ringkasan di bagian bawah ekspor tidak boleh 'menempel' ke pesanan sebelumnya."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_baris_total_tidak_dihitung_sebagai_item(self):
        isi = ("No. Pesanan,SKU,Nama Produk,Jumlah\n"
              "T1,SKU-A,Barang A,2\n"
              ",,Grand Total,99\n")
        f = tulis(self.dir, "pesanan.csv", isi)
        kode, data, _, err = jalankan(f, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, err)
        self.assertEqual(data["jumlah_sku_unik"], 1)
        self.assertEqual(data["total_barang"], 2.0)
        self.assertEqual(data["baris_dilewati"].get("baris_ringkasan_diabaikan"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
