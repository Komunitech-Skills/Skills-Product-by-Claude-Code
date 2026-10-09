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


if __name__ == "__main__":
    unittest.main(verbosity=2)
