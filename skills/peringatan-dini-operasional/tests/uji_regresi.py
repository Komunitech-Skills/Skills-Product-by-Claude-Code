#!/usr/bin/env python3
"""Uji regresi peringatan-dini-operasional.
Jalankan: python3 tests/uji_regresi.py   (Windows: py tests/uji_regresi.py)

Angka acuan dihitung manual (lihat komentar tiap tes), bukan disalin dari keluaran script:
  rata-rata      = jumlah / n
  sigma sampel   = akar( jumlah (x - rata)^2 / (n - 1) )
  z              = (nilai hari ini - rata garis dasar) / sigma
  kemiringan     = jumlah (x - x_rata)(y - y_rata) / jumlah (x - x_rata)^2
  sisa hari stok = stok / rata-rata pemakaian 7 hari, dibulatkan ke BAWAH 1 desimal
"""
import contextlib
import io
import math
import os
import random
import sys
import tempfile
import unittest
import zipfile
from datetime import date, timedelta
from decimal import Decimal as D

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import peringatan_dini as P  # noqa: E402

MULAI = date(2026, 9, 1)  # Selasa


def tabel(kolom, deret, mulai=MULAI, target=None, ekstra=None):
    """kolom = ['reject'], deret = {'reject': [..]} -> tabel baris (list of list)."""
    n = max(len(v) for v in deret.values())
    t = [["tanggal"] + kolom]
    if target:
        t.append(["TARGET"] + [target.get(k, "") for k in kolom])
    for i in range(n):
        t.append([(mulai + timedelta(days=i)).isoformat()] + [str(deret[k][i]) if i < len(deret[k]) and deret[k][i] is not None else "" for k in kolom])
    if ekstra:
        t.extend(ekstra)
    return t


def jalankan(t, *opsi):
    args = P.buat_parser().parse_args(["-"] + list(opsi))
    return P.analisis(t, args)


def metrik(hasil, kolom):
    return next(m for m in hasil["metrik"] if m["kolom"] == kolom)


def bulat(x, d=4):
    return D(x).quantize(D(1).scaleb(-d))


class Parsing(unittest.TestCase):
    def test_angka_gaya_indonesia(self):
        kasus = {"1.250": 1250, "1,5": D("1.5"), "1,2rb": 1200, "Rp 1.250.000": 1250000, "2,5%": D("2.5"),
                 "1.250,5": D("1250.5"), "1,250.5": D("1250.5"), "1.2jt": 1200000, "1.250rb": 1250000,
                 "15.000,-": 15000, "0,25": D("0.25"), "0.250": D("0.25"), "63": 63, "2.1rb": 2100,
                 "IDR 9.000.000": 9000000, "9,1jt": 9100000, "12.5": D("12.5"), "-3": -3}
        for teks, harap in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(P.parse_angka(teks), D(harap))

    def test_angka_kosong_dan_rusak(self):
        for teks in ("", "-", "libur", "Tutup", "n/a", None):
            self.assertIsNone(P.parse_angka(teks))
        for teks in ("abc", "1.2.3", "1,5E+06", "12..5", "Rp", "1.25.000"):
            with self.subTest(teks=teks):
                with self.assertRaises(P.InputError):
                    P.parse_angka(teks)

    def test_koma_tiga_digit_dicatat_ambigu(self):
        amb = []
        self.assertEqual(P.parse_angka("1,250", amb), D(1250))
        self.assertEqual(amb, ["1,250"])

    def test_tanggal(self):
        kasus = {"2026-09-29": date(2026, 9, 29), "29/09/2026": date(2026, 9, 29), "29-9-26": date(2026, 9, 29),
                 "29 Sep 2026": date(2026, 9, 29), "1 Agustus 2026": date(2026, 8, 1),
                 "Selasa, 29 September 2026": date(2026, 9, 29), "2026-09-29 07:00": date(2026, 9, 29),
                 D(46294): date(2026, 9, 29)}  # nomor seri Excel: 1899-12-30 + 46294 hari
        for teks, harap in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(P.parse_tanggal(teks), harap)
        self.assertEqual(P.parse_tanggal("09/29/2026", "mdy"), date(2026, 9, 29))
        with self.assertRaises(P.InputError):
            P.parse_tanggal("31/02/2026")

    def test_tabel_tempel_garis_tegak(self):
        teks = "| Tanggal | Reject |\n|---|---|\n| 1/9/2026 | 30 |\n| 2/9/2026 | 1.250 |\n"
        self.assertEqual(P.baca_teks(teks), [["Tanggal", "Reject"], ["1/9/2026", "30"], ["2/9/2026", "1.250"]])

    def test_delimiter_titik_koma_dan_komentar(self):
        teks = "# komentar\ntanggal;penjualan_rp\n2026-09-01;1.250.000\n"
        self.assertEqual(P.baca_teks(teks), [["tanggal", "penjualan_rp"], ["2026-09-01", "1.250.000"]])

    def test_arah_tebakan(self):
        kasus = {"telat_kirim": "naik", "output_pcs": "turun", "tidak_hadir": "naik", "hadir": "turun",
                 "suhu_oven": "dua", "pesanan_batal": "naik", "reject_pcs": "naik", "penjualan_rp": "turun",
                 "keluhan": "naik", "absen": "naik"}
        for n, harap in kasus.items():
            with self.subTest(n=n):
                self.assertEqual(P.tebak_arah(n), harap)

    def test_label(self):
        self.assertEqual(P.label_cantik("stok_tepung_kg"), "Stok tepung (kg)")
        self.assertEqual(P.label_cantik("penjualan_rp"), "Penjualan (Rp)")
        self.assertEqual(P.label_cantik("Reject Harian"), "Reject Harian")


class Statistik(unittest.TestCase):
    # Garis dasar 14 hari: 8,12,8,12,... (7 kali 8 dan 7 kali 12).
    # rata = 10; tiap selisih ±2 -> jumlah kuadrat 14 x 4 = 56; varians = 56/13 = 4,307692;
    # sigma = 2,075498; hari ke-15 (Selasa 15 Sep) = 16 -> z = 6 / 2,075498 = 2,8909
    DASAR = [8, 12] * 7
    # v1.0.1: angka bulat dengan rata-rata < 20 memakai model hitungan (Poisson) untuk ATURAN warna
    # (temuan penguji #2: 16 vs rata 10 wajar untuk hitungan kecil). Statistik σ/z tetap dihitung.
    # Untuk menguji aturan σ dipakai deret yang sama x10 (rata 100 -> model normal):
    # rata 100, sigma 20,75498; 160 -> z 2,8909; 170 -> z 3,3727; 190 -> z 4,3363.
    DASAR10 = [80, 120] * 7

    def test_sigma_dan_z(self):
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR + [16]})), "reject")
        self.assertEqual(m["dasar"]["n"], 14)
        self.assertEqual(bulat(m["dasar"]["rata"]), D("10.0000"))
        self.assertEqual(bulat(m["dasar"]["sd"]), D("2.0755"))
        self.assertEqual(bulat(m["z"]), D("2.8909"))
        self.assertEqual(bulat(m["dasar"]["batas_atas_2"]), D("14.1510"))   # 10 + 2 x 2,075498
        self.assertEqual(bulat(m["dasar"]["batas_atas_3"]), D("16.2265"))   # 10 + 3 x 2,075498
        # model hitungan: P(X >= 16 | lambda 10) = 0,049 > 0,0228 -> tidak ada alarm σ
        self.assertEqual(m["model"], "hitungan")
        self.assertFalse(any("σ" in t for _, t in m["alasan"]))
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR10 + [160]})), "reject")
        self.assertEqual(m["model"], "normal")
        self.assertEqual(bulat(m["z"]), D("2.8909"))
        self.assertTrue(any("2,9σ" in t and "waspada" in t for _, t in m["alasan"]))
        self.assertEqual(m["level"], 1)  # v1.0.1: 2σ satu hari saja = kuning (dulu oranye)

    def test_tiga_sigma_merah(self):
        # v1.0.1: 3σ satu hari = oranye; merah bila >= 4σ, atau 3σ dan kemarin juga >= 2σ
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR10 + [170]})), "reject")
        self.assertEqual(bulat(m["z"]), D("3.3727"))
        self.assertEqual(m["level"], 2)
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR10 + [190]})), "reject")
        self.assertEqual(bulat(m["z"]), D("4.3363"))
        self.assertEqual(m["level"], 3)
        # kemarin 160 (2,9σ terhadap garis dasar hari ini) lalu hari ini 185 -> bertahan -> merah
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR10 + [160, 185]})), "reject")
        self.assertGreaterEqual(m["z"], 3)
        self.assertLess(m["z"], D("3.9"))
        self.assertEqual(m["level"], 3)
        self.assertTrue(any("2 dari 3 hari" in t for _, t in m["alasan"]))

    def test_dua_sigma_bertahan_oranye(self):
        # 2σ dua hari berturut-turut -> oranye (satu hari saja -> kuning)
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR10 + [155, 158]})), "reject")
        self.assertGreaterEqual(m["z"], 2)
        self.assertLess(m["z"], 3)
        self.assertEqual(m["level"], 2)

    def test_tren_kemiringan(self):
        # 7 hari terakhir (9-15 Sep): 8,12,8,12,8,12,16 ; x = 0..6 ; x_rata = 3 ; Sxx = 28
        # Sxy = -3x8 -2x12 -1x8 +0x12 +1x8 +2x12 +3x16 = 24 -> kemiringan 24/28 = 0,857143
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR + [16]})), "reject")
        self.assertEqual(m["tren"]["n"], 7)
        self.assertEqual(bulat(m["tren"]["kemiringan_per_hari"]), D("0.8571"))

    def test_tren_dengan_hari_bolong(self):
        # hari 0,1,3,4 bernilai 10,12,16,18 (hari ke-2 kosong) -> garis lurus, kemiringan 2, R² 1
        b, r2 = P.regresi([(0, D(10)), (1, D(12)), (3, D(16)), (4, D(18))])
        self.assertEqual(b, D(2))
        self.assertEqual(r2, D(1))

    def test_rata7_dan_hari_sama(self):
        # rata 7 terakhir (9-15 Sep) = 76/7 = 10,857143 ; 7 sebelumnya (2-8 Sep) = 12,8,12,8,12,8,12 = 72/7
        # perubahan = (76-72)/72 x 100 = 5,5556%
        # hari yang sama (Selasa) 8 Sep = 12 dan 1 Sep = 8 -> rata 10 ; 16 vs 10 = +60%
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR + [16]})), "reject")
        self.assertEqual(bulat(m["rata7"]), D("10.8571"))
        self.assertEqual(bulat(m["perubahan7_persen"]), D("5.5556"))
        self.assertEqual(m["hari_sama"]["n"], 2)
        self.assertEqual(bulat(m["hari_sama"]["rata"]), D("10.0000"))
        self.assertEqual(bulat(m["hari_sama"]["selisih_persen"]), D("60.0000"))
        # v1.0.1: rata hari sama 10 < 5? tidak; tapi hitungan kecil: selisih 6 < 2 x akar(10) = 6,32 -> tidak kuning
        self.assertFalse(any("rata-rata hari" in t for _, t in m["alasan"]))
        # x10: 160 vs 100 = +60% dan selisih 60 >= 2 x 20,755 -> kuning (aturan hari-sama kini maks kuning)
        m = metrik(jalankan(tabel(["reject"], {"reject": self.DASAR10 + [160]})), "reject")
        self.assertTrue(any(lv == 1 and "60% di atas rata-rata hari Selasa" in t for lv, t in m["alasan"]))

    def test_pencilan_dibuang_sekali(self):
        # 18 angka 9,11,... (rata 10) + 1 angka 40 di hari ke-19 -> tahap 1: rata 220/19 = 11,5789,
        # sigma 6,955, z(40) = 4,09 > 3 -> dibuang. Tahap 2: rata 10, sigma = akar(18/17) = 1,0290.
        deret = [9, 11] * 9 + [40] + [10]
        m = metrik(jalankan(tabel(["reject"], {"reject": deret})), "reject")
        self.assertEqual(m["dasar"]["pencilan_diabaikan"], [(MULAI + timedelta(days=18)).isoformat()])
        self.assertEqual(m["dasar"]["n"], 18)
        self.assertEqual(bulat(m["dasar"]["rata"]), D("10.0000"))
        self.assertEqual(bulat(m["dasar"]["sd"]), D("1.0290"))

    def test_beruntun_naik(self):
        # 20,21,22,23 -> 3 kenaikan berturut-turut
        titik = [(MULAI + timedelta(days=i), D(v)) for i, v in enumerate([25, 20, 21, 22, 23])]
        self.assertEqual(P.beruntun(titik, "naik"), 3)
        self.assertEqual(P.beruntun(titik, "turun"), 0)
        # celah > 3 hari memutus urutan
        titik2 = [(MULAI, D(1)), (MULAI + timedelta(days=5), D(2)), (MULAI + timedelta(days=6), D(3))]
        self.assertEqual(P.beruntun(titik2, "naik"), 1)

    def test_proyeksi_ke_target(self):
        # 14 hari datar 30,32 lalu 7 hari: 30,32,34,36,38,40,42 ; target maks 50 ; kemiringan 2, R² 1
        # (50 - 42) / 2 = 4 hari -> kuning "±4 hari"
        deret = [30, 32] * 7 + [30, 32, 34, 36, 38, 40, 42]
        m = metrik(jalankan(tabel(["reject"], {"reject": deret}, target={"reject": "50"})), "reject")
        self.assertEqual(bulat(m["proyeksi_hari_ke_target"]), D("4.0000"))
        self.assertTrue(any("±4 hari" in t for _, t in m["alasan"]))

    def test_target_naik_dan_turun(self):
        dasar = [30, 32] * 7
        # 76 vs maks 50 -> +52% -> merah
        m = metrik(jalankan(tabel(["reject"], {"reject": dasar + [76]}, target={"reject": "50"})), "reject")
        self.assertEqual(m["level"], 3)
        self.assertEqual(bulat(m["target_info"]["selisih_persen"]), D("52.0000"))
        # output 1.900 vs min 2.000 -> -5% -> kuning (tidak ada aturan lain yang kena)
        out = [2000, 2040] * 7 + [1900]
        m = metrik(jalankan(tabel(["output"], {"output": out}, target={"output": "2.000"})), "output")
        self.assertEqual(bulat(m["target_info"]["selisih_persen"]), D("-5.0000"))
        self.assertTrue(any("di bawah target min" in t for _, t in m["alasan"]))

    def test_persen_kecil_tidak_dipakai(self):
        # keluhan rata hari yang sama 1 (< 5) -> aturan persen tidak dipakai walau +100%
        kel = [1, 0, 1, 1, 0, 1, 1] * 2 + [2]
        m = metrik(jalankan(tabel(["keluhan"], {"keluhan": kel})), "keluhan")
        self.assertFalse(any("rata-rata hari" in t for _, t in m["alasan"]))


class Stok(unittest.TestCase):
    def test_sisa_hari_dari_kolom_pakai(self):
        # pakai 7 hari terakhir: 60,70,70,80,70,70,70 -> rata 490/7 = 70 ; stok 180 -> 2,571 -> 2,5 (ke bawah)
        stok = [600, 540, 470, 400, 320, 250, 180]
        pakai = [60, 70, 70, 80, 70, 70, 70]
        h = jalankan(tabel(["stok_tepung", "pakai_tepung"], {"stok_tepung": stok, "pakai_tepung": pakai}))
        s = metrik(h, "stok_tepung")
        self.assertEqual(s["rata_pakai"], D(70))
        self.assertEqual(s["sisa_hari"], D("2.5"))
        # v1.0.1 (temuan penguji #4): stok akhir 2,57 hari -> 2 hari penuh (cukup sampai +2),
        # mulai kurang di hari ke-3 (+3). Dulu "habis" = +floor = +2.
        self.assertEqual(s["cukup_sampai"], (MULAI + timedelta(days=6 + 2)).isoformat())
        self.assertEqual(s["perkiraan_habis"], (MULAI + timedelta(days=6 + 3)).isoformat())
        self.assertEqual(s["level"], 2)  # 2,5 <= 2 x lead 2
        h = jalankan(tabel(["stok_tepung", "pakai_tepung"], {"stok_tepung": stok, "pakai_tepung": pakai}), "--lead-time", "3")
        self.assertEqual(metrik(h, "stok_tepung")["level"], 3)  # 2,5 <= 3
        self.assertFalse(any(m["kolom"] == "pakai_tepung" for m in h["metrik"]))

    def test_stok_kurang_dari_sehari(self):
        # stok 45, pemakaian 50/hari -> 0,9 hari: "habis besok", bukan tanggal hari ini (temuan #4)
        h = jalankan(tabel(["stok_kopi", "pakai_kopi"], {"stok_kopi": [200, 150, 95, 45], "pakai_kopi": [50, 50, 55, 50]}))
        s = metrik(h, "stok_kopi")
        self.assertEqual(s["sisa_hari"], D("0.8"))  # 45 / 51,25 = 0,878 -> 0,8
        self.assertEqual(s["perkiraan_habis"], (MULAI + timedelta(days=4)).isoformat())
        self.assertIsNone(s["cukup_sampai"])
        teks = s["alasan"][0][1]
        self.assertIn("habis besok", teks)
        self.assertIn("kemungkinan kosong", teks)
        self.assertEqual(s["level"], 3)

    def test_stok_pakai_nol_bukan_normal(self):
        h = jalankan(tabel(["stok_kain_m", "pakai_kain_m"], {"stok_kain_m": [100] * 5, "pakai_kain_m": [0] * 5}))
        self.assertNotIn("Stok kain (m)", h["laporan_teks"].split("✅ Normal:")[-1].split("\n")[0]
                         if "✅ Normal:" in h["laporan_teks"] else "")
        self.assertIn("belum bisa dihitung", h["laporan_teks"])

    def test_sisa_hari_tanpa_kolom_pakai(self):
        # penurunan harian 50,60,60,60 (hari restok +370 diabaikan) -> rata 57,5 ; 580/57,5 = 10,08 -> 10,0
        h = jalankan(tabel(["stok_gula"], {"stok_gula": [500, 450, 390, 700, 640, 580]}))
        s = metrik(h, "stok_gula")
        self.assertEqual(s["rata_pakai"], D("57.5"))
        self.assertEqual(s["sisa_hari"], D("10.0"))
        self.assertEqual(s["level"], 0)
        self.assertIn("perkiraan", s["sumber_pemakaian"])


class DataBuruk(unittest.TestCase):
    def test_data_sedikit(self):
        h = jalankan(tabel(["reject"], {"reject": [30, 31, 29, 33, 35]}))
        m = metrik(h, "reject")
        self.assertTrue(h["data_sedikit"])
        self.assertNotIn("z", m)
        self.assertTrue(any("batas kendali" in b for b in m["butuh_data"]))
        self.assertIn("Data baru 5 hari", h["laporan_teks"])

    def test_hari_kosong_dan_libur(self):
        deret = [30, 31, None, 29, 33]
        t = tabel(["reject"], {"reject": deret})
        h = jalankan(t)
        self.assertEqual(h["kualitas_data"]["hari_kosong"], [(MULAI + timedelta(days=2)).isoformat()])
        self.assertEqual(h["kualitas_data"]["hari_tercatat"], 4)

    def test_tidak_diisi_hari_ini(self):
        t = tabel(["reject", "keluhan"], {"reject": [30, 31, 29], "keluhan": [1, 2, None]})
        h = jalankan(t)
        self.assertIn("Keluhan", h["kualitas_data"]["tidak_diisi_hari_ini"])
        self.assertIn("Belum diisi hari ini: Keluhan", h["laporan_teks"])

    def test_log_belum_diisi_tidak_dibilang_aman(self):
        h = jalankan(tabel(["reject"], {"reject": [30, 31, 29]}), "--tanggal", "2026-09-05")
        self.assertTrue(h["belum_diisi"])
        self.assertIn("BELUM DIISI", h["laporan_teks"])
        self.assertNotIn("Tidak ada tanda bahaya", h["laporan_teks"])

    def test_duplikat_dan_sel_rusak(self):
        t = [["tanggal", "reject"], ["2026-09-01", "10"], ["2026-09-01", "5"], ["2026-09-02", "abc"],
             ["2026-09-03", "-4"], ["2026-09-04", "12"], ["bukan tanggal", "9"]]
        h = jalankan(t)
        self.assertEqual(metrik(h, "reject")["n"], 2)       # 1 Sep (baris terakhir = 5) & 4 Sep
        self.assertEqual(len(h["kualitas_data"]["sel_rusak"]), 2)
        self.assertEqual(len(h["kualitas_data"]["baris_dilewati"]), 1)
        self.assertEqual(h["kualitas_data"]["tanggal_duplikat"], ["2026-09-01"])
        h2 = jalankan(t, "--duplikat", "jumlah")
        self.assertEqual(metrik(h2, "reject")["n"], 2)
        # nilai 1 Sep = 10 + 5 = 15
        args = P.buat_parser().parse_args(["-", "--duplikat", "jumlah"])
        data = P.susun_data(t, args, [])
        self.assertEqual(data["kolom"][0]["nilai"][date(2026, 9, 1)], D(15))

    def test_kolom_teks_tidak_dikutip(self):
        # temuan penguji #3: kolom nama karyawan tidak boleh ikut ke laporan
        t = tabel(["karyawan_absen", "jumlah_absen"], {"karyawan_absen": ["Budi"] * 5, "jumlah_absen": [1, 0, 1, 2, 1]})
        h = jalankan(t)
        self.assertNotIn("Budi", h["laporan_teks"])
        self.assertNotIn("Budi", str(h["catatan_hari_ini"]))
        self.assertTrue(any("karyawan_absen" in c for c in h["catatan"]))

    def test_target_nol_tanpa_persen(self):
        h = jalankan(tabel(["keluhan"], {"keluhan": [0, 0, 0, 1]}, target={"keluhan": "0"}))
        m = metrik(h, "keluhan")
        self.assertEqual(m["level"], 2)
        self.assertFalse(any("%" in t for _, t in m["alasan"]))

    def test_abaikan_tanggal(self):
        h = jalankan(tabel(["reject"], {"reject": [30, 31, 99, 29]}), "--abaikan-tanggal", "2026-09-03")
        self.assertEqual(metrik(h, "reject")["n"], 3)

    def test_tanpa_kolom_angka(self):
        with self.assertRaises(P.InputError):
            jalankan([["tanggal", "catatan"], ["2026-09-01", "aman"]])
        with self.assertRaises(P.InputError):
            jalankan([["tanggal", "reject"]])

    def test_rasio_reject_otomatis(self):
        # reject 40 / output 2000 x 100 = 2%
        h = jalankan(tabel(["output_pcs", "reject_pcs"], {"output_pcs": [2000, 1000], "reject_pcs": [40, 30]}))
        m = metrik(h, "persen_reject")
        self.assertEqual(m["terbaru"]["nilai"], D(3))
        self.assertEqual(m["arah"], "naik")


def poisson_acak(r, lam):
    """Bilangan Poisson (algoritma Knuth), hanya untuk membuat data uji."""
    batas, k, prod = math.exp(-lam), 0, 1.0
    while True:
        prod *= r.random()
        if prod < batas:
            return k
        k += 1


class KeandalanAlarm(unittest.TestCase):
    """v1.0.1 -- temuan penguji #1 (alarm terlewat) dan #2 (alarm palsu)."""

    def test_ekor_poisson_manual(self):
        # P(X >= 2 | 1) = 1 - e^-1 (1 + 1) = 0,2642411 ; P(X <= 0 | 2) = e^-2 = 0,1353353
        self.assertAlmostEqual(P.ekor_poisson(2, 1, "naik"), 0.2642411, places=6)
        self.assertAlmostEqual(P.ekor_poisson(0, 2, "turun"), 0.1353353, places=6)
        # P(X >= 16 | 10) = 0,0487404 (tabel Poisson)
        self.assertAlmostEqual(P.ekor_poisson(16, 10, "naik"), 0.0487404, places=6)

    def test_alarm_palsu_data_stabil(self):
        # Log stabil 6 kolom (+ % reject otomatis), 45 hari, TANPA perubahan apa pun; dinilai hari ke-31..45.
        # Syarat: hari dengan >= oranye <= 5%, hari dengan merah <= 1%. (v1.0.0: 31% dan 5,9%.)
        kolom = ["output_pcs", "reject_pcs", "penjualan_rp", "keluhan", "telat_kirim", "absen", "retur"]
        hari = oranye = merah = 0
        for benih in range(40):
            r = random.Random(1000 + benih)
            t = [["tanggal"] + kolom]
            for i in range(45):
                t.append([(MULAI + timedelta(days=i)).isoformat(), str(round(r.gauss(2000, 60))),
                          str(poisson_acak(r, 30)), str(round(r.gauss(9e6, 4e5))), str(poisson_acak(r, 0.7)),
                          str(poisson_acak(r, 7)), str(poisson_acak(r, 1.2)), str(poisson_acak(r, 15))])
            for d in range(30, 45):
                h = jalankan(t, "--tanggal", (MULAI + timedelta(days=d)).isoformat())
                mx = max(m["level"] for m in h["metrik"])
                hari += 1
                oranye += mx >= 2
                merah += mx >= 3
        self.assertLessEqual(oranye / hari, 0.05, f"oranye+ {oranye}/{hari}")
        self.assertLessEqual(merah / hari, 0.01, f"merah {merah}/{hari}")

    def test_alarm_tidak_terlewat_garis_dasar_nol(self):
        # 20 hari keluhan 0, kecelakaan 0, output selalu 100; hari ini keluhan 6, kecelakaan 2, output 0
        t = tabel(["keluhan", "kecelakaan_kerja", "output"],
                  {"keluhan": [0] * 20 + [6], "kecelakaan_kerja": [0] * 20 + [2], "output": [100] * 20 + [0]})
        h = jalankan(t)
        self.assertEqual(metrik(h, "keluhan")["level"], 3)
        self.assertEqual(metrik(h, "kecelakaan_kerja")["level"], 3)
        self.assertEqual(metrik(h, "kecelakaan_kerja")["model"], "kejadian")
        self.assertEqual(metrik(h, "output")["level"], 3)
        self.assertNotIn("✅ Normal", h["laporan_teks"])
        # satu keluhan setelah 20 hari nol -> minimal kuning, bukan "Normal"
        h = jalankan(tabel(["keluhan"], {"keluhan": [0] * 20 + [1]}))
        self.assertEqual(metrik(h, "keluhan")["level"], 1)
        # dua keluhan -> oranye; satu angka 1 di masa lalu tidak membuat alarm hilang
        h = jalankan(tabel(["keluhan"], {"keluhan": [0] * 9 + [1] + [0] * 10 + [2]}))
        self.assertEqual(metrik(h, "keluhan")["level"], 2)
        # --kejadian untuk kolom bernama bebas
        h = jalankan(tabel(["mesin_rusak"], {"mesin_rusak": [0] * 10 + [1]}), "--kejadian", "mesin_rusak")
        self.assertEqual(metrik(h, "mesin_rusak")["level"], 3)

    def test_sensitivitas_tetap(self):
        # output normal 2000 +- 60 lalu turun 10% dua hari -> minimal oranye pada hari ke-2
        r = random.Random(5)
        out = [round(r.gauss(2000, 60)) for _ in range(28)] + [1800, 1800]
        h = jalankan(tabel(["output_pcs"], {"output_pcs": out}))
        self.assertGreaterEqual(metrik(h, "output_pcs")["level"], 2)

    def test_sigma_sangat_kecil_butuh_selisih_bermakna(self):
        # penjualan hampir konstan: selisih 1% tidak memicu alarm walau z besar (temuan penguji #6)
        jual = [9000000, 9010000] * 10 + [8910000]
        h = jalankan(tabel(["penjualan_rp"], {"penjualan_rp": jual}))
        self.assertEqual(metrik(h, "penjualan_rp")["level"], 0)


class BerkasDanLaporan(unittest.TestCase):
    def test_xlsx_minimal(self):
        ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        rns = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        sheet = (f'<worksheet {ns}><sheetData>'
                 '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>'
                 '<row r="2"><c r="A2"><v>46266</v></c><c r="B2"><v>1250.125</v></c></row>'
                 '<row r="3"><c r="A3"><v>46267</v></c><c r="B3" t="inlineStr"><is><t>1.300</t></is></c></row>'
                 '</sheetData></worksheet>')
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "log.xlsx")
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("xl/workbook.xml", f'<workbook {ns} {rns}><sheets><sheet name="Log" sheetId="1" r:id="rId1"/></sheets></workbook>')
                z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
                z.writestr("xl/sharedStrings.xml", f'<sst {ns}><si><t>Tanggal</t></si><si><t>Output</t></si></sst>')
                z.writestr("xl/worksheets/sheet1.xml", sheet)
            t = P.baca_tabel(p)
        self.assertEqual(t[0], ["Tanggal", "Output"])
        self.assertEqual(P.parse_tanggal(t[1][0]), date(2026, 9, 1))   # 1899-12-30 + 46266 hari
        self.assertEqual(P.parse_angka(t[1][1]), D("1250.125"))         # sel angka Excel tidak ditafsir ulang
        self.assertEqual(P.parse_angka(t[2][1]), D(1300))

    def test_contoh_roti_30_hari(self):
        p = os.path.join(AKAR, "examples", "log-roti-30hari.csv")
        args = P.buat_parser().parse_args([p])
        h = P.analisis(P.baca_tabel(p), args)
        rj = metrik(h, "reject_pcs")
        self.assertEqual(rj["level"], 3)
        self.assertEqual(rj["dasar"]["pencilan_diabaikan"], ["2026-09-07"])
        self.assertEqual(h["kualitas_data"]["hari_kosong"], ["2026-09-13"])
        st = metrik(h, "stok_tepung_kg")
        self.assertEqual(st["level"], 2)
        # pemakaian 7 hari terakhir 23-29 Sep: 51,52,56,57,50,50,50 = 366/7 = 52,2857 ; 169/52,2857 = 3,23 -> 3,2
        self.assertEqual(bulat(st["rata_pakai"]), D("52.2857"))
        self.assertEqual(st["sisa_hari"], D("3.2"))
        teks = h["laporan_teks"]
        for frasa in ("🔴 Reject (pcs): 63", "laporan-insiden-usaha", "bukan kepastian"):
            self.assertIn(frasa, teks)
        # v1.0.1 (temuan penguji #3): catatan teks tidak dikutip kecuali --sertakan-catatan
        self.assertNotIn("oven 2 suhu tidak stabil", teks)
        self.assertEqual(h["catatan_hari_ini"], ["oven 2 suhu tidak stabil siang"])
        h2 = P.analisis(P.baca_tabel(p), P.buat_parser().parse_args([p, "--sertakan-catatan"]))
        self.assertIn("oven 2 suhu tidak stabil", h2["laporan_teks"])
        self.assertLessEqual(len(teks.splitlines()), 40)

    def test_cli_kode_keluar(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "kosong.csv")
            open(p, "w").close()
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(P.main([p]), 2)
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(P.main([os.path.join(AKAR, "examples", "log-roti-30hari.csv"), "--format", "json"]), 0)
            self.assertIn('"tanggal_laporan": "2026-09-29"', out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=1)
