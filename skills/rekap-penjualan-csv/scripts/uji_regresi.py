#!/usr/bin/env python3
"""Uji regresi rekap.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rekap.py")


def rekap(isi_csv, *arg):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "jual.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(isi_csv)
        r = subprocess.run([sys.executable, SCRIPT, path, "--kolom-tanggal", "Tanggal", "--kolom-produk", "Produk",
                            "--kolom-total", "Total"] + list(arg), capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout) if r.returncode == 0 else None)


# 01/09: 1 pesanan besar (omzet tertinggi); 02/09: 3 pesanan kecil (transaksi terbanyak, 4 baris)
CSV = """No. Pesanan,Tanggal,Produk,Total
A1,01/09/2026,Serum,500.000
B1,02/09/2026,Masker,20.000
B1,02/09/2026,Sabun,10.000
B2,02/09/2026,Masker,20.000
B3,02/09/2026,Sabun,10.000
C1,03/09/2026,Masker,20.000
"""


class Uji(unittest.TestCase):
    def test_hari_omzet_vs_transaksi_terbanyak(self):
        # Temuan uji OpenClaw 2026-10-01: "hari paling rame" hanya dijawab dari omzet.
        _, h = rekap(CSV)
        self.assertEqual(h["hari_terbaik"]["tanggal"], "2026-09-01")
        self.assertEqual(h["hari_transaksi_terbanyak"]["tanggal"], "2026-09-02")
        self.assertEqual(h["hari_transaksi_terbanyak"]["jumlah"], 4)
        self.assertEqual(h["hari_transaksi_terbanyak"]["satuan"], "baris transaksi")
        self.assertEqual(h["jumlah_transaksi_harian"], {"2026-09-01": 1, "2026-09-02": 4, "2026-09-03": 1})

    def test_pesanan_unik(self):
        _, h = rekap(CSV, "--kolom-pesanan", "No. Pesanan")
        self.assertEqual(h["hari_transaksi_terbanyak"]["jumlah"], 3)
        self.assertIn("pesanan unik", h["hari_transaksi_terbanyak"]["satuan"])
        self.assertEqual(h["total_omzet"], 580000)

    def test_seri(self):
        _, h = rekap(CSV.replace("C1,03/09/2026,Masker,20.000\n", "") + "C1,03/09/2026,Masker,20.000\n" * 4)
        self.assertEqual(h["hari_transaksi_terbanyak"]["semua_tanggal_seri"], ["2026-09-02", "2026-09-03"])

    def test_kolom_pesanan_tidak_ada(self):
        r, _ = rekap(CSV, "--kolom-pesanan", "Order ID")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Order ID", r.stdout + r.stderr)


# Ekspor gaya Shopee FIKTIF (uji gabungan toko-online 2026-10-02): 15 Selesai, 3 Sedang Dikirim, 2 Dibatalkan.
# Nama & nomor di bawah fiktif; dipakai untuk memastikan ringkasan grup tidak memuat data pribadi.
SHOPEE = """No. Pesanan,Status Pesanan,Waktu Pesanan Dibuat,Nama Produk,Jumlah,Harga Satuan,Total Harga Produk,Ongkos Kirim Dibayar Pembeli,Nama Penerima,No. Telepon,Kota/Kabupaten
260928A1B2C3,Selesai,2026-09-28 08:15,Kaos Polos Cotton Combed 30s Hitam,2,"65.000","130.000","12.000",Rina Marlina,6281234500101,KOTA BANDUNG
260928A1B2C4,Selesai,2026-09-28 10:42,Hoodie Fleece Navy,1,"175.000","175.000","15.000",Andi Saputra,6281398700202,KOTA BEKASI
260928A1B2C5,Dibatalkan,2026-09-28 13:05,Kaos Polos Cotton Combed 30s Putih,3,"65.000","195.000","12.000",Dewi Lestari,6285711100303,KAB. BOGOR
260928A1B2C6,Selesai,2026-09-28 19:30,Celana Jogger Abu,1,"120.000","120.000","10.000",Budi Hartono,6281277700404,KOTA SURABAYA
260929D4E5F6,Selesai,2026-09-29 07:55,Kaos Polos Cotton Combed 30s Hitam,4,"65.000","260.000","18.000",Siti Aminah,6287855500505,KOTA MALANG
260929D4E5F7,Selesai,2026-09-29 11:20,Hoodie Fleece Navy,2,"175.000","350.000","15.000",Rina Marlina,6281234500101,KOTA BANDUNG
260929D4E5F8,Selesai,2026-09-29 15:10,Topi Baseball Bordir,3,"45.000","135.000","9.000",Yusuf Maulana,6281933300606,KOTA SEMARANG
260929D4E5F9,Sedang Dikirim,2026-09-29 21:45,Celana Jogger Abu,2,"120.000","240.000","12.000",Fitri Handayani,6285266600707,KOTA MEDAN
260930G7H8I9,Selesai,2026-09-30 09:00,Kaos Polos Cotton Combed 30s Putih,5,"65.000","325.000","20.000",Agus Salim,6281144400808,KOTA DEPOK
260930G7H8J1,Selesai,2026-09-30 12:35,Topi Baseball Bordir,1,"45.000","45.000","9.000",Maya Sari,6281355500909,KOTA YOGYAKARTA
260930G7H8J2,Dibatalkan,2026-09-30 16:50,Hoodie Fleece Navy,1,"175.000","175.000","15.000",Hendra Wijaya,6281566601010,KOTA TANGERANG
260930G7H8J3,Selesai,2026-09-30 20:05,Kaos Polos Cotton Combed 30s Hitam,1,"65.000","65.000","10.000",Andi Saputra,6281398700202,KOTA BEKASI
261001K1L2M3,Selesai,2026-10-01 08:40,Celana Jogger Abu,1,"120.000","120.000","10.000",Lina Kurniawati,6281277701111,KOTA SURABAYA
261001K1L2M4,Selesai,2026-10-01 10:15,Hoodie Fleece Navy,1,"175.000","175.000","15.000",Siti Aminah,6287855500505,KOTA MALANG
261001K1L2M5,Sedang Dikirim,2026-10-01 14:25,Kaos Polos Cotton Combed 30s Hitam,3,"65.000","195.000","12.000",Rudi Hermawan,6281788801212,KOTA BANDUNG
261001K1L2M6,Selesai,2026-10-01 19:50,Topi Baseball Bordir,2,"45.000","90.000","9.000",Dewi Lestari,6285711100303,KAB. BOGOR
261002N4O5P6,Selesai,2026-10-02 07:30,Kaos Polos Cotton Combed 30s Putih,2,"65.000","130.000","12.000",Wahyu Pratama,6281999901313,KOTA SOLO
261002N4O5P7,Selesai,2026-10-02 09:45,Celana Jogger Abu,1,"120.000","120.000","10.000",Rina Marlina,6281234500101,KOTA BANDUNG
261002N4O5P8,Sedang Dikirim,2026-10-02 13:15,Hoodie Fleece Navy,1,"175.000","175.000","15.000",Nur Hidayah,6285677701414,KOTA PALEMBANG
261002N4O5P9,Selesai,2026-10-02 16:00,Kaos Polos Cotton Combed 30s Hitam,2,"65.000","130.000","12.000",Yusuf Maulana,6281933300606,KOTA SEMARANG
"""
ARG_SHOPEE = ["--kolom-tanggal", "Waktu Pesanan Dibuat", "--kolom-produk", "Nama Produk", "--kolom-qty", "Jumlah",
              "--kolom-total", "Total Harga Produk", "--kolom-status", "Status Pesanan", "--kolom-pesanan", "No. Pesanan"]


def rekap_shopee(*tambahan):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "shopee.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(SHOPEE)
        r = subprocess.run([sys.executable, SCRIPT, path] + ARG_SHOPEE + list(tambahan),
                           capture_output=True, text=True, encoding="utf-8")
    return json.loads(r.stdout)


def pembanding_independen():
    """Hitung ulang TANPA kode rekap.py: csv standar + int sederhana (titik = ribuan)."""
    import csv, io
    per_status, batal_tgl, pesanan_ok = {}, {}, set()
    for r in csv.DictReader(io.StringIO(SHOPEE)):
        st, no, tgl = r["Status Pesanan"], r["No. Pesanan"], r["Waktu Pesanan Dibuat"][:10]
        nilai = int(r["Total Harga Produk"].replace(".", ""))
        d = per_status.setdefault(st, {"pesanan": set(), "omzet": 0})
        d["pesanan"].add(no)
        d["omzet"] += nilai
        if st == "Dibatalkan":
            batal_tgl[tgl] = batal_tgl.get(tgl, 0) + 1
        else:
            pesanan_ok.add(no)
    return per_status, batal_tgl, pesanan_ok


class UjiPerStatus(unittest.TestCase):
    # Temuan uji gabungan 2026-10-02: agent mengarang nilai "Sedang Dikirim" (~Rp440rb, benar Rp610rb)
    # dan hari pembatalan, karena script tidak mengeluarkan angka per status.
    def test_per_status_cocok_pembanding(self):
        h = rekap_shopee()
        per_status, _, pesanan_ok = pembanding_independen()
        self.assertEqual(set(h["per_status"]), set(per_status))
        for st, v in per_status.items():
            self.assertEqual(h["per_status"][st]["omzet"], v["omzet"], st)
            self.assertEqual(h["per_status"][st]["jumlah_pesanan"], len(v["pesanan"]), st)
        self.assertEqual(h["per_status"]["Sedang Dikirim"]["omzet"], 610000)
        self.assertEqual(h["per_status"]["Dibatalkan"]["golongan"], "dibuang")
        self.assertFalse(h["per_status"]["Sedang Dikirim"]["final"])
        self.assertTrue(h["per_status"]["Selesai"]["final"])
        self.assertEqual(h["jumlah_pesanan_dihitung"], len(pesanan_ok))
        self.assertEqual(h["total_omzet"], per_status["Selesai"]["omzet"] + per_status["Sedang Dikirim"]["omzet"])

    def test_tanggal_pembatalan(self):
        h = rekap_shopee()
        _, batal_tgl, _ = pembanding_independen()
        self.assertEqual({x["tanggal"]: x["jumlah_pesanan"] for x in h["dibuang_per_tanggal"]}, batal_tgl)
        self.assertEqual(batal_tgl, {"2026-09-28": 1, "2026-09-30": 1})

    def test_ringkasan_siap_tempel_tanpa_data_pribadi(self):
        import csv, io
        h = rekap_shopee()
        teks = h["ringkasan_siap_tempel"]
        self.assertTrue(teks.startswith("RINGKASAN SIAP TEMPEL"))
        for kata in ("Rp 2.980.000", "Sedang Dikirim 3 pesanan senilai Rp 610.000", "28 Sep 2026 1 pesanan",
                     "30 Sep 2026 1 pesanan", "Dibatalkan 2 pesanan", "(tidak masuk omzet)", "belum final"):
            self.assertIn(kata, teks)
        for r in csv.DictReader(io.StringIO(SHOPEE)):
            for kolom in ("Nama Penerima", "No. Telepon", "No. Pesanan"):
                self.assertNotIn(r[kolom], teks)
            self.assertNotIn(r["No. Telepon"][-6:], teks)
        for baris in teks.splitlines()[1:]:
            self.assertTrue(baris.endswith("."), baris)  # kalimat lengkap

    def test_tanpa_kolom_status_tetap_ada_ringkasan(self):
        _, h = rekap(CSV)
        self.assertEqual(h["per_status"], {})
        self.assertIn("Rp 580.000", h["ringkasan_siap_tempel"])


    def test_data_rusak_tidak_crash(self):
        rusak = ("Tanggal;Produk;Qty;Harga;Status\n01/09/2026;Kopi;2;Rp 15.000;Selesai\nxx;Teh;1;10.000;Batal\n"
                 "02/09/2026;Teh;abc;10.000;Selesai\n02/09/2026;Kopi;1;15.000.00;Dikirim\n")
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "rusak.csv")
            with open(path, "w", encoding="utf-8") as f:
                f.write(rusak)
            r = subprocess.run([sys.executable, SCRIPT, path, "--kolom-tanggal", "Tanggal", "--kolom-produk", "Produk",
                                "--kolom-qty", "Qty", "--kolom-harga", "Harga", "--kolom-status", "Status"],
                               capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stderr)
        h = json.loads(r.stdout)
        self.assertEqual(h["total_omzet"], 30000)
        self.assertEqual(h["baris_dilewati"], 2)
        self.assertEqual(h["per_status"]["Batal"]["omzet"], 10000)
        self.assertEqual(h["dibuang_per_tanggal"][0]["tanggal"], "(tanggal tidak terbaca)")
        self.assertIn("2 baris tidak terbaca", h["ringkasan_siap_tempel"])


# ---------------------------------------------------------------------------------------------------------------
# Uji bot Telegram asli 17 Okt 2026 (gelombang A5): dengan skill 6,5 BELUM karena insight dikarang dan bertentangan
# dengan tabel ("Topi Baseball qty terjual paling banyak ... harganya paling murah"; benar: Tote Bag Natural 23 pcs,
# Rp 35.000), memakai "margin" tanpa data modal, terlaris per jumlah tidak disebut, format chat terlalu berat.
# CSV FIKTIF di bawah dibuat ulang agar angka agregatnya sama dengan data uji itu: 72 baris; Selesai 66 pesanan
# Rp 5.519.000, Batal 4 Rp 238.000, Pengembalian Dana 2 Rp 272.000; 29 hari berjualan; tertinggi 5 Sep Rp 549.000;
# terendah 18 Sep Rp 35.000; pesanan terbanyak 1 & 5 Sep (5). Tanpa nama/nomor pembeli.
PRODUK_SEP = {"OA": ("Kaos Oversize Abu", 79000), "PP": ("Kaos Polos Putih", 59000),
              "PH": ("Kaos Polos Hitam", 59000), "TP": ("Topi Baseball", 45000), "TO": ("Tote Bag Natural", 35000)}
# tanggal -> pesanan Selesai "KODE*qty" (satu produk per pesanan); 20 Sep tidak ada penjualan
SELESAI_SEP = {
    1: "PH*1 TP*1 TO*1 TO*1 TP*2", 2: "PH*2 TO*1 TO*1", 3: "OA*1", 4: "PP*1 OA*1 TP*2",
    5: "OA*3 PP*2 PH*1 TP*2 TP*1", 6: "TP*1 TP*1", 7: "OA*3", 8: "TO*2", 9: "PP*1 TP*1", 10: "TO*1 PH*1",
    11: "OA*1 PP*2 PH*2", 12: "PH*1 TP*2", 13: "TO*2 PH*1", 14: "OA*3 PP*3 TO*2", 15: "TP*2 PP*1",
    16: "TP*1 PH*1 OA*3", 17: "PP*2 TO*1 TO*1 TO*1", 18: "TO*1", 19: "TO*1 TO*2 TP*1", 21: "PP*2 OA*1",
    22: "TO*1 OA*2", 23: "TP*3", 24: "PH*1", 25: "TP*1 PH*1 PH*1", 26: "TO*3", 27: "TP*1 PP*3 TO*1 PP*1",
    28: "OA*3", 29: "PH*2 PH*1", 30: "PH*1",
}
DIBUANG_SEP = [(2, "Batal", "OA*1"), (10, "Batal", "TP*1"), (11, "Pengembalian Dana", "OA*3"),
               (25, "Batal", "TO*1"), (26, "Batal", "OA*1"), (28, "Pengembalian Dana", "TO*1")]
ARG_SEP = ["--kolom-tanggal", "Waktu Pesanan Dibuat", "--kolom-produk", "Nama Produk", "--kolom-qty", "Jumlah",
           "--kolom-total", "Total Harga Produk", "--kolom-status", "Status Pesanan", "--kolom-pesanan", "No. Pesanan"]


def pesanan_september():
    """Daftar (tanggal, status, kode, qty) urut tanggal; dipakai CSV dan pembanding independen."""
    hasil = []
    for d in range(1, 31):
        for item in SELESAI_SEP.get(d, "").split():
            kode, q = item.split("*")
            hasil.append((d, "Selesai", kode, int(q)))
        for dd, st, item in DIBUANG_SEP:
            if dd == d:
                kode, q = item.split("*")
                hasil.append((d, st, kode, int(q)))
    return hasil


def csv_september():
    baris = ["No. Pesanan,Status Pesanan,Waktu Pesanan Dibuat,Nama Produk,Jumlah,Harga Satuan,Total Harga Produk"]
    urutan_hari = {}
    for n, (d, st, kode, q) in enumerate(pesanan_september(), 1):
        i = urutan_hari[d] = urutan_hari.get(d, -1) + 1
        nama, harga = PRODUK_SEP[kode]
        baris.append("2609{:02d}KT{:03d},{},2026-09-{:02d} {:02d}:{:02d},{},{},{},{}".format(
            d, n, st, d, 8 + 2 * i, (17 * n) % 60, nama, q,
            "{:,}".format(harga).replace(",", "."), "{:,}".format(harga * q).replace(",", ".")))
    return "\n".join(baris) + "\n"


def rekap_september(*tambahan):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "penjualan-september.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(csv_september())
        r = subprocess.run([sys.executable, SCRIPT, path] + ARG_SEP + list(tambahan),
                           capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def pembanding_produk_september():
    """Hitung ulang per produk TANPA rekap.py: int murni dari spesifikasi pesanan."""
    per = {}
    for _, st, kode, q in pesanan_september():
        if st != "Selesai":
            continue
        nama, harga = PRODUK_SEP[kode]
        d = per.setdefault(nama, {"qty": 0, "omzet": 0, "harga": harga})
        d["qty"] += q
        d["omzet"] += harga * q
    return per


class UjiSorotanProdukSeptember(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h = rekap_september()
        cls.per = pembanding_produk_september()

    def test_data_fiktif_sama_dengan_angka_kunci_uji_a5(self):
        h = self.h
        self.assertEqual(len(csv_september().strip().splitlines()) - 1, 72)
        ps = h["per_status"]
        self.assertEqual((ps["Selesai"]["jumlah_pesanan"], ps["Selesai"]["omzet"]), (66, 5519000))
        self.assertEqual((ps["Batal"]["jumlah_pesanan"], ps["Batal"]["omzet"]), (4, 238000))
        self.assertEqual((ps["Pengembalian Dana"]["jumlah_pesanan"], ps["Pengembalian Dana"]["omzet"]), (2, 272000))
        self.assertEqual(h["total_omzet"], 5519000)
        self.assertEqual({k: (v["omzet"], v["qty"], v["harga"]) for k, v in self.per.items()}, {
            "Kaos Oversize Abu": (1659000, 21, 79000), "Kaos Polos Putih": (1062000, 18, 59000),
            "Kaos Polos Hitam": (1003000, 17, 59000), "Topi Baseball": (990000, 22, 45000),
            "Tote Bag Natural": (805000, 23, 35000)})
        self.assertEqual(h["periode"]["jumlah_hari_kalender"], 30)
        self.assertEqual(h["periode"]["jumlah_hari_ada_penjualan"], 29)
        self.assertEqual(h["hari_terbaik"], {"tanggal": "2026-09-05", "omzet": 549000})
        self.assertEqual(h["hari_terendah"], {"tanggal": "2026-09-18", "omzet": 35000})
        self.assertEqual(h["hari_transaksi_terbanyak"]["semua_tanggal_seri"], ["2026-09-01", "2026-09-05"])
        self.assertEqual(h["hari_transaksi_terbanyak"]["jumlah"], 5)
        self.assertEqual(sorted({x["tanggal"][-2:] for x in h["dibuang_per_tanggal"]}),
                         ["02", "10", "11", "25", "26", "28"])

    def test_terlaris_menurut_omzet_dan_jumlah(self):
        s = self.h["sorotan_produk"]
        top_q = max(self.per.values(), key=lambda v: v["qty"])
        self.assertEqual([x["produk"] for x in s["terlaris_qty"]], ["Tote Bag Natural"])
        self.assertEqual(s["terlaris_qty"][0]["qty"], top_q["qty"])
        self.assertEqual(s["terlaris_qty"][0]["qty"], 23)
        self.assertEqual(s["terlaris_qty"][0]["peringkat_omzet"], 5)
        self.assertEqual([x["produk"] for x in s["terlaris_omzet"]], ["Kaos Oversize Abu"])
        self.assertEqual(s["terlaris_omzet"][0]["omzet"], 1659000)
        self.assertFalse(s["terlaris_omzet_dan_qty_sama"])
        self.assertEqual([x["produk"] for x in self.h["produk_terlaris_qty"]],
                         ["Tote Bag Natural", "Topi Baseball", "Kaos Oversize Abu", "Kaos Polos Putih",
                          "Kaos Polos Hitam"])
        self.assertEqual([x["produk"] for x in self.h["produk_terlaris"]],
                         ["Kaos Oversize Abu", "Kaos Polos Putih", "Kaos Polos Hitam", "Topi Baseball",
                          "Tote Bag Natural"])

    def test_harga_jual_per_pcs_termurah_termahal(self):
        s = self.h["sorotan_produk"]
        for x in self.h["produk_terlaris"]:
            self.assertEqual(x["harga_per_pcs"], self.per[x["produk"]]["harga"], x["produk"])
            self.assertFalse(x["harga_per_pcs_bervariasi"])
        self.assertEqual([(x["produk"], x["harga_per_pcs"]) for x in s["harga_per_pcs_termurah"]],
                         [("Tote Bag Natural", 35000)])
        self.assertEqual([(x["produk"], x["harga_per_pcs"]) for x in s["harga_per_pcs_termahal"]],
                         [("Kaos Oversize Abu", 79000)])

    def test_fakta_insight_tidak_bertentangan_dengan_angka(self):
        fakta = self.h["fakta_produk"]
        self.assertIn("Terlaris menurut omzet: Kaos Oversize Abu, Rp 1.659.000 (30,1% dari omzet), 21 pcs.", fakta)
        self.assertIn("Terlaris menurut jumlah: Tote Bag Natural, 23 pcs (Rp 805.000; peringkat 5 menurut omzet "
                      "dari 5 produk).", fakta)
        self.assertIn("Tote Bag Natural paling banyak terjual (23 pcs) tetapi omzetnya di bawah Kaos Oversize Abu "
                      "(Rp 805.000 vs Rp 1.659.000) karena harga jual per pcs-nya lebih rendah (Rp 35.000 vs "
                      "Rp 79.000).", fakta)
        self.assertIn("Harga jual per pcs dari 5 produk: termurah Tote Bag Natural (Rp 35.000); termahal "
                      "Kaos Oversize Abu (Rp 79.000).", fakta)
        # Cacat bot 17 Okt: Topi Baseball disebut terbanyak & termurah. Tidak boleh ada di keluaran mana pun.
        for teks in fakta + [self.h["rekap_chat"], self.h["ringkasan_siap_tempel"]]:
            for kalimat in teks.replace("\n", ". ").split(". "):
                if "Topi Baseball" in kalimat:
                    for kata in ("paling", "termurah", "termahal", "terlaris menurut jumlah"):
                        self.assertNotIn(kata, kalimat.lower(), kalimat)

    def test_rekap_chat_ringan_satu_rata_rata(self):
        teks = self.h["rekap_chat"]
        for baris in teks.splitlines():
            self.assertFalse(baris.lstrip().startswith("#"), baris)
            self.assertNotIn("|", baris)
            self.assertNotIn("**", baris)
            self.assertFalse(baris.startswith("_"), baris)
        self.assertEqual(teks.lower().count("rata-rata"), 1)
        self.assertIn("Rata-rata per hari: Rp 183.967 (omzet dibagi 30 hari kalender; 29 hari ada penjualan)", teks)
        self.assertNotIn("190.310", teks)                     # rata-rata kedua (hari berjualan) tidak tampil
        self.assertEqual(self.h["rata_rata_harian"]["dasar"], "hari kalender")
        for kata in ("Omzet: Rp 5.519.000 dari 66 pesanan Selesai",
                     "Tidak dihitung (batal/retur): ", "Batal 4 pesanan Rp 238.000",
                     "Pengembalian Dana 2 pesanan Rp 272.000",
                     "1. Kaos Oversize Abu: Rp 1.659.000 (30,1%), 21 pcs × Rp 79.000",
                     "4. Topi Baseball: Rp 990.000 (17,9%), 22 pcs × Rp 45.000",
                     "5. Tote Bag Natural: Rp 805.000 (14,6%), 23 pcs × Rp 35.000",
                     "Terlaris menurut jumlah: Tote Bag Natural, 23 pcs",
                     "Omzet tertinggi 5 Sep 2026 (Rp 549.000); terendah 18 Sep 2026 (Rp 35.000)",
                     "Pesanan terbanyak: 1 Sep 2026 dan 5 Sep 2026 (5 pesanan per hari, seri)"):
            self.assertIn(kata, teks)
        self.assertLess(len(teks), 1200)
        self.assertIn("Paling banyak terjual menurut jumlah: Tote Bag Natural (23 pcs).",
                      self.h["ringkasan_siap_tempel"])

    def test_tanpa_kata_margin_atau_laba(self):
        semua = " ".join([self.h["rekap_chat"], self.h["ringkasan_siap_tempel"]] + self.h["fakta_produk"]).lower()
        for kata in ("margin", "laba", "untung", "profit"):
            self.assertNotIn(kata, semua)


class UjiSeriDanHargaBervariasi(unittest.TestCase):
    def test_seri_jumlah_dan_harga_rata_rata(self):
        isi = ("Tanggal,Produk,Qty,Total\n01/09/2026,Kopi,3,30.000\n01/09/2026,Teh,2,10.000\n"
               "02/09/2026,Teh,1,6.000\n02/09/2026,Roti,3,45.000\n")
        _, h = rekap(isi, "--kolom-qty", "Qty")
        s = h["sorotan_produk"]
        self.assertEqual(sorted(x["produk"] for x in s["terlaris_qty"]), ["Kopi", "Roti", "Teh"])
        self.assertEqual([x["produk"] for x in s["terlaris_omzet"]], ["Roti"])
        teh = [x for x in h["produk_terlaris"] if x["produk"] == "Teh"][0]
        self.assertTrue(teh["harga_per_pcs_bervariasi"])               # Rp 5.000 dan Rp 6.000 per pcs
        self.assertAlmostEqual(teh["harga_per_pcs"], 16000 / 3, places=2)
        self.assertIn("Teh: Rp 16.000 (17,6%), 3 pcs, rata-rata Rp 5.333/pcs", h["rekap_chat"])
        self.assertTrue(any("(seri)" in f for f in h["fakta_produk"]))
        self.assertIn("masing-masing", h["rekap_chat"])
        # Tidak ada kalimat "X paling banyak terjual ... karena" saat seri (tidak bisa disimpulkan satu produk)
        self.assertFalse(any("karena" in f for f in h["fakta_produk"]))
        self.assertEqual([x["produk"] for x in s["harga_per_pcs_termurah"]], ["Teh"])
        self.assertEqual([x["produk"] for x in s["harga_per_pcs_termahal"]], ["Roti"])

    def test_satu_produk_tanpa_perbandingan_harga(self):
        _, h = rekap("Tanggal,Produk,Total\n01/09/2026,Kopi,10.000\n02/09/2026,Kopi,12.000\n")
        s = h["sorotan_produk"]
        self.assertEqual(s["harga_per_pcs_termurah"], [])
        self.assertIsNone(s["terlaris_omzet_dan_qty_sama"])           # tanpa kolom jumlah: pcs tidak diketahui
        self.assertTrue(s["terlaris_omzet_dan_baris_sama"])
        self.assertIn("catatan", s)
        self.assertFalse(any("termurah" in f for f in h["fakta_produk"]))
        self.assertIn("Paling sering tercatat juga Kopi (2 baris transaksi)", h["rekap_chat"])

    def test_terlaris_jumlah_sama_dengan_omzet(self):
        _, h = rekap("Tanggal,Produk,Qty,Total\n01/09/2026,Kopi,3,30.000\n01/09/2026,Teh,1,5.000\n", "--kolom-qty", "Qty")
        self.assertTrue(h["sorotan_produk"]["terlaris_omzet_dan_qty_sama"])
        self.assertIn("Terlaris menurut jumlah juga Kopi (3 pcs)", h["rekap_chat"])
        self.assertIn("Terlaris menurut jumlah juga Kopi (3 pcs).", h["fakta_produk"])


# ---------------------------------------------------------------------------------------------------------------
# Temuan verifikator 1.2.6 (putaran 1): file TANPA kolom jumlah (mis. spreadsheet Tanggal,Produk,Total) tetap
# ditulis "2 pcs", "× Rp X", harga per pcs termurah/termahal, dan "terlaris menurut jumlah", padahal tiap baris
# hanya DIANGGAP 1 pcs. Bila 1 baris berisi beberapa unit, saran harga jadi salah (cacat sejenis uji bot asli).
TANPA_QTY = ("Tanggal,Produk,Total\n01/09/2026,Kopi Susu,54.000\n01/09/2026,Teh Manis,40.000\n"
             "02/09/2026,Kopi Susu,18.000\n02/09/2026,Roti Bakar,15.000\n03/09/2026,Roti Bakar,15.000\n")


def teks_keluaran(h):
    return [h["rekap_chat"], h["ringkasan_siap_tempel"]] + h["fakta_produk"]


class UjiTanpaKolomJumlah(unittest.TestCase):
    def test_tanpa_qty_tidak_mengklaim_pcs_atau_harga_per_pcs(self):
        import csv, io, re
        _, h = rekap(TANPA_QTY)
        self.assertEqual(h["satuan_jumlah_produk"], "baris transaksi")
        s = h["sorotan_produk"]
        self.assertEqual((s["terlaris_qty"], s["harga_per_pcs_termurah"], s["harga_per_pcs_termahal"]), ([], [], []))
        self.assertEqual(h["produk_terlaris_qty"], [])
        for x in h["produk_terlaris"]:
            self.assertIsNone(x["harga_per_pcs"], x["produk"])
            self.assertIsNone(x["peringkat_qty"], x["produk"])
            self.assertFalse(x["harga_per_pcs_bervariasi"], x["produk"])
        # jumlah baris per produk dicek independen dengan csv standar
        baris = {}
        for r in csv.DictReader(io.StringIO(TANPA_QTY)):
            baris[r["Produk"]] = baris.get(r["Produk"], 0) + 1
        self.assertEqual({x["produk"]: x["jumlah_baris"] for x in h["produk_terlaris"]}, baris)
        self.assertEqual([x["produk"] for x in s["terlaris_baris"]], ["Kopi Susu", "Roti Bakar"])
        self.assertFalse(s["terlaris_omzet_dan_baris_sama"])
        self.assertIn("--satu-baris-satu-pcs", s["catatan"])
        for teks in teks_keluaran(h):
            self.assertIsNone(re.search(r"\d pcs", teks), teks)
            for kata in ("/pcs", "×", "termurah", "termahal", "karena", "Terlaris menurut jumlah",
                         "Paling banyak terjual", "Harga jual per pcs dari"):
                self.assertNotIn(kata, teks)
        chat = h["rekap_chat"]
        for kata in ("1. Kopi Susu: Rp 72.000 (50,7%), 2 baris transaksi",
                     "2. Teh Manis: Rp 40.000 (28,2%), 1 baris transaksi",
                     "Paling sering tercatat: Kopi Susu dan Roti Bakar, 2 baris transaksi masing-masing",
                     "Catatan data: file tanpa kolom jumlah, jadi jumlah pcs dan harga jual per pcs tidak diketahui"):
            self.assertIn(kata, chat)
        self.assertIn("Catatan: file tanpa kolom jumlah, jadi jumlah pcs yang terjual tidak diketahui.",
                      h["ringkasan_siap_tempel"])

    def test_seri_peringkat_ditulis_lengkap_tanpa_garis_miring(self):
        _, h = rekap(TANPA_QTY)
        kalimat = [f for f in h["fakta_produk"] if f.startswith("Paling sering tercatat")]
        self.assertEqual(kalimat, ["Paling sering tercatat (jumlah baris transaksi, bukan pcs; seri): Kopi Susu dan "
                                   "Roti Bakar, 2 baris transaksi masing-masing (Kopi Susu Rp 72.000, peringkat 1 "
                                   "menurut omzet; Roti Bakar Rp 30.000, peringkat 3 menurut omzet; dari 3 produk)."])
        for f in h["fakta_produk"]:
            self.assertNotIn("1/3", f)
            self.assertNotIn("/Rp", f)

    def test_satu_baris_satu_pcs_setelah_konfirmasi_pengguna(self):
        _, h = rekap(TANPA_QTY, "--satu-baris-satu-pcs")
        s = h["sorotan_produk"]
        self.assertEqual(h["satuan_jumlah_produk"], "pcs")
        self.assertEqual([(x["produk"], x["qty"]) for x in s["terlaris_qty"]], [("Kopi Susu", 2), ("Roti Bakar", 2)])
        self.assertEqual([(x["produk"], x["harga_per_pcs"]) for x in s["harga_per_pcs_termurah"]], [("Roti Bakar", 15000)])
        self.assertEqual([(x["produk"], x["harga_per_pcs"]) for x in s["harga_per_pcs_termahal"]], [("Teh Manis", 40000)])
        self.assertIn("Catatan data: tiap baris dihitung 1 pcs (sesuai konfirmasi Anda)", h["rekap_chat"])
        self.assertIn("Terlaris menurut jumlah (seri): Kopi Susu dan Roti Bakar, 2 pcs masing-masing (Kopi Susu "
                      "Rp 72.000, peringkat 1 menurut omzet; Roti Bakar Rp 30.000, peringkat 3 menurut omzet; dari "
                      "3 produk).", h["fakta_produk"])

    def test_opsi_satu_baris_tidak_mengubah_kolom_qty(self):
        isi = "Tanggal,Produk,Qty,Total\n01/09/2026,Kopi,3,30.000\n01/09/2026,Teh,2,10.000\n"
        _, a = rekap(isi, "--kolom-qty", "Qty")
        _, b = rekap(isi, "--kolom-qty", "Qty", "--satu-baris-satu-pcs")
        self.assertEqual(a["produk_terlaris"], b["produk_terlaris"])
        self.assertNotIn("catatan", b["sorotan_produk"])
        self.assertNotIn("Catatan data", b["rekap_chat"])


class UjiStatusBelumFinal(unittest.TestCase):
    # Temuan verifikator 1.2.6: bila hanya SATU status dihitung dan belum final (mis. semua "Sedang Dikirim"),
    # rekap_chat tidak menyebut "belum final", padahal SKILL.md menyuruh rekap_chat ditempel apa adanya.
    ISI = ("No,Tanggal,Produk,Qty,Total,Status\n"
           "P1,01/09/2026,Kaos,2,100.000,Sedang Dikirim\nP2,02/09/2026,Topi,1,45.000,Sedang Dikirim\n"
           "P3,02/09/2026,Kaos,1,50.000,Dibatalkan\n")

    def test_satu_status_belum_final_disebut_di_rekap_chat(self):
        _, h = rekap(self.ISI, "--kolom-qty", "Qty", "--kolom-status", "Status", "--kolom-pesanan", "No")
        self.assertFalse(h["per_status"]["Sedang Dikirim"]["final"])
        self.assertIn("Omzet: Rp 145.000 dari 2 pesanan Sedang Dikirim (belum final, bisa berubah bila batal/retur)",
                      h["rekap_chat"])

    def test_satu_status_final_tanpa_keterangan(self):
        _, h = rekap(self.ISI.replace("Sedang Dikirim", "Selesai"), "--kolom-qty", "Qty", "--kolom-status", "Status",
                     "--kolom-pesanan", "No")
        self.assertIn("Omzet: Rp 145.000 dari 2 pesanan Selesai\n", h["rekap_chat"])
        self.assertNotIn("belum final", h["rekap_chat"])


class UjiVersi(unittest.TestCase):
    def test_versi_sama_di_script_dan_dokumen(self):
        sys.path.insert(0, os.path.dirname(SCRIPT))
        import rekap as modul
        self.assertEqual(modul.VERSI, "1.2.6")
        r = subprocess.run([sys.executable, SCRIPT, "--versi"], capture_output=True, text=True)
        self.assertIn("1.2.6", r.stdout + r.stderr)
        _, h = rekap(CSV)
        self.assertEqual(h["versi_script"], "1.2.6")
        folder = os.path.dirname(os.path.dirname(SCRIPT))
        for nama in ("SKILL.md", "README.md", "CHANGELOG.md"):
            with open(os.path.join(folder, nama), encoding="utf-8") as f:
                self.assertTrue("1.2.6" in f.read(), nama)

    def test_contoh_readme_sama_dengan_keluaran_rekap_chat(self):
        # Temuan verifikator 1.2.6: cuplikan README masih format lama (judul ##, tabel, dua rata-rata).
        with open(os.path.join(os.path.dirname(os.path.dirname(SCRIPT)), "README.md"), encoding="utf-8") as f:
            isi = f.read()
        blok = isi.split("## Contoh sebelum & sesudah", 1)[1].split("\n## ", 1)[0].split("```")[1]
        chat = rekap_september()["rekap_chat"]
        baris_isi = [b for b in blok.splitlines() if b.strip() and b.strip() != "…"]
        self.assertGreater(len(baris_isi), 8)
        for b in baris_isi:
            self.assertFalse(b.lstrip().startswith("#"), b)
            self.assertNotIn("|", b)
            self.assertNotIn("**", b)
            self.assertIn(b, chat.splitlines(), b)

    def test_format_chat_di_skill_md_tanpa_judul_markdown(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(SCRIPT)), "SKILL.md"), encoding="utf-8") as f:
            isi = f.read()
        blok = isi.split("## Format output", 1)[1].split("```", 2)[1]
        for baris in blok.splitlines():
            self.assertFalse(baris.lstrip().startswith("#"), baris)
            self.assertNotIn("|", baris)


if __name__ == "__main__":
    unittest.main(verbosity=2)
