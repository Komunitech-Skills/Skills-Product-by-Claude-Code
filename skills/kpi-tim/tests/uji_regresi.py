#!/usr/bin/env python3
"""Uji regresi kpi-tim. Jalankan: python3 tests/uji_regresi.py   (Windows: py tests/uji_regresi.py)

Semua angka diverifikasi dengan tangan (rumus di komentar), bukan disalin dari output script.
Rumus:
  naik : capaian = realisasi / target x 100
  turun: capaian = (2 - realisasi / target) x 100 ; target 0 -> 100 jika realisasi 0, selain itu 0
  capaian dipakai = dibatasi 0..120 (atau maks_capai baris)
  skor orang = jumlah(bobot x capaian dipakai) / 100
Data contoh: templates/rencana-kpi-contoh.csv + templates/realisasi-contoh.csv (distributor fiktif, 8 orang).
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from decimal import Decimal

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import skor_kpi as K  # noqa: E402

TPL = os.path.join(AKAR, "templates")
RENCANA = os.path.join(TPL, "rencana-kpi-contoh.csv")
REALISASI = os.path.join(TPL, "realisasi-contoh.csv")


def jalan(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        kode = K.main(list(argv) + ["--json"])
    return kode, json.loads(buf.getvalue())


def D(s):
    return Decimal(s) if s is not None else None


def r1(s):
    """String JSON (4 desimal) -> dibulatkan 1 desimal seperti tampilan."""
    return K.bulat(Decimal(s), 1) if s is not None else None


class Dasar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def file(self, nama, isi):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write(isi)
        return p

    def skor(self, *extra, rencana=RENCANA, realisasi=REALISASI):
        kode, out = jalan("skor", "--rencana", rencana, "--realisasi", realisasi, *extra)
        return kode, out

    def orang(self, out, nama):
        return next(o for o in out["orang"] if o["nama"] == nama)


class UjiAngka(unittest.TestCase):
    def test_format_indonesia(self):
        self.assertEqual(K.angka("1.250.000"), Decimal("1250000"))
        self.assertEqual(K.angka("12,5"), Decimal("12.5"))
        self.assertEqual(K.angka("Rp 1.250.000,50"), Decimal("1250000.50"))
        self.assertEqual(K.angka("0.955"), Decimal("0.955"))   # bukan 955: grup pertama '0'
        self.assertEqual(K.angka("85%"), Decimal("85"))
        self.assertEqual(K.angka("3,5x"), Decimal("3.5"))
        self.assertEqual(K.angka("1,250"), Decimal("1.25"))     # koma tunggal = desimal (gaya Indonesia)
        self.assertEqual(K.angka("1,250,000"), Decimal("1250000"))
        self.assertEqual(K.angka("-4"), Decimal("-4"))
        self.assertIsNone(K.angka(""))
        self.assertEqual(K.angka(K.Num("12.345")), Decimal("12.345"))  # sel XLSX: titik = desimal
        with self.assertRaises(K.Gagal):
            K.angka("dua belas")

    def test_capaian_arah(self):
        cap = Decimal(120)
        # naik: 162/150 = 1,08 -> 108
        self.assertEqual(K.hitung_capaian("naik", D("150"), D("162"), cap), (D("108"), D("108")))
        # turun: (2 - 8/10) x 100 = 120
        self.assertEqual(K.hitung_capaian("turun", D("10"), D("8"), cap)[1], D("120"))
        # turun: (2 - 15/10) x 100 = 50
        self.assertEqual(K.hitung_capaian("turun", D("10"), D("15"), cap)[1], D("50"))
        # turun: (2 - 25/10) x 100 = -50 -> dibatasi 0
        self.assertEqual(K.hitung_capaian("turun", D("10"), D("25"), cap), (D("-50"), D("0")))
        # turun target 0: realisasi 0 -> 100, realisasi 1 -> 0
        self.assertEqual(K.hitung_capaian("turun", D("0"), D("0"), cap)[1], D("100"))
        self.assertEqual(K.hitung_capaian("turun", D("0"), D("1"), cap)[1], D("0"))
        # cap: 2 - 0/3 = 200 -> 120
        self.assertEqual(K.hitung_capaian("turun", D("3"), D("0"), cap), (D("200"), D("120")))


class UjiContohDistributor(Dasar):
    def test_skor_september(self):
        kode, out = self.skor("--periode", "2026-09")
        self.assertEqual(kode, 0, out)
        self.assertEqual(out["periode_lalu"], "2026-08")
        # Andi: .4x108 + .25x(14/15=93,333) + .2x(14/50=28% -> 112) + .15x(81/90=90)
        #     = 43,2 + 23,3333 + 22,4 + 13,5 = 102,4333
        andi = self.orang(out, "Andi Pratama")
        self.assertEqual(r1(andi["skor"]), D("102.4"))
        self.assertEqual(D(andi["skor"]).quantize(D("0.0001")), D("102.4333"))
        # Rina: .4x80 + .25x60 + .2x80 + .15x(92/90=102,222) = 32+15+16+15,3333 = 78,3333
        rina = self.orang(out, "Rina Wulandari")
        self.assertEqual(r1(rina["skor"]), D("78.3"))
        self.assertEqual(rina["status"], "merah")
        omzet_rina = next(k for k in rina["kpi"] if k["kpi"] == "Omzet penjualan")
        self.assertEqual(omzet_rina["status"], "merah")      # 96 jt < ambang 100 jt
        # Dewi: .3x120 + .3x(95/90=105,556) + .25x(4,6/4,7=97,872) + .15x(97/95=102,105) = 107,4506
        dewi = self.orang(out, "Dewi Lestari")
        self.assertEqual(r1(dewi["skor"]), D("107.5"))
        rating = next(k for k in dewi["kpi"] if k["kpi"] == "Rating kepuasan")
        self.assertEqual(rating["status"], "kuning")          # 4,6 >= ambang 4,5, < target 4,7
        # Budi: .35x(98,5/99=99,495) + .3x(96/95=101,053) + .2x(2-2/3=133,3 -> 120) + .15x(2-4/5=120) = 107,139
        self.assertEqual(r1(self.orang(out, "Budi Santoso")["skor"]), D("107.1"))
        # Joko: .35x96,970 + .3x92,632 + .2x(2-6/3=0) + .15x100 = 33,939+27,789+0+15 = 76,729
        joko = self.orang(out, "Joko Susilo")
        self.assertEqual(r1(joko["skor"]), D("76.7"))
        akurasi = next(k for k in joko["kpi"] if k["kpi"] == "Akurasi stok")
        self.assertEqual(akurasi["status"], "merah")           # 96 < ambang 97
        # Eko: .4x(91/95=95,789) + .25x(2-4/3=66,667) + .2x(640/600=106,667) + .15x100 = 91,3158
        self.assertEqual(r1(self.orang(out, "Eko Saputra")["skor"]), D("91.3"))
        # Sari: .3x(2-6/5=80) + .3x(2-12/10=80) + .2x(100/95=105,263) + .2x(2-0=200 -> 120) = 93,0526
        self.assertEqual(r1(self.orang(out, "Sari Indah")["skor"]), D("93.1"))
        # Tono: Nota diarsip belum ada -> mode tandai: skor kosong
        tono = self.orang(out, "Tono Wijaya")
        self.assertIsNone(tono["skor"])
        self.assertEqual(tono["status"], "belum")
        self.assertEqual(tono["kurang"], ["Nota diarsip lengkap"])
        # sementara = (40x94,444 + 30x120 + 15x105,263) / 85 = 8956,73/85 = 105,373
        self.assertEqual(r1(tono["skor_sementara"]), D("105.4"))
        # Divisi = rata-rata individu lengkap
        div = {d["nama"]: d for d in out["divisi"]}
        # Sales (102,4333 + 78,3333 + 107,4506)/3 = 96,0724
        self.assertEqual(r1(div["Sales"]["skor"]), D("96.1"))
        # Gudang (107,139 + 76,7289 + 91,3158)/3 = 91,7279
        self.assertEqual(r1(div["Gudang & Pengiriman"]["skor"]), D("91.7"))
        # Keuangan & Admin: hanya Sari (Tono belum lengkap) = 93,0526, ditandai sebagian
        self.assertEqual(r1(div["Keuangan & Admin"]["skor"]), D("93.1"))
        self.assertTrue(div["Keuangan & Admin"]["sebagian"])
        # Perusahaan (96,0724 + 91,7279 + 93,0526)/3 = 93,6176
        self.assertEqual(r1(out["perusahaan"]["skor"]), D("93.6"))
        self.assertTrue(out["perusahaan"]["sebagian"])
        self.assertTrue(any("Tono Wijaya belum lengkap" in w for w in out["peringatan"]))

    def test_tren_vs_agustus(self):
        kode, out = self.skor("--periode", "2026-09")
        # Andi Agustus: .4x94 + .25x86,667 + .2x(13/52=25% -> 100) + .15x94,444 = 93,4333 -> tren +9,0
        self.assertEqual(r1(self.orang(out, "Andi Pratama")["tren"]), D("9.0"))
        # Sari Agustus: .3x60 + .3x60 + .2x100 + .2x(2-1,5=50) = 66 -> tren 93,0526-66 = +27,1
        self.assertEqual(r1(self.orang(out, "Sari Indah")["tren"]), D("27.1"))
        # Tono belum lengkap -> tidak ada tren
        self.assertIsNone(self.orang(out, "Tono Wijaya")["tren"])

    def test_periode_default_terbaru(self):
        kode, out = self.skor()
        self.assertEqual(out["periode"], "2026-09")

    def test_bobot_ulang_dan_nol(self):
        kode, out = self.skor("--periode", "2026-09", "--data-kosong", "bobot-ulang")
        tono = self.orang(out, "Tono Wijaya")
        self.assertEqual(r1(tono["skor"]), D("105.4"))           # 8956,73/85
        self.assertEqual(tono["dasar"], "bobot-ulang")
        # Keuangan & Admin = (93,0526 + 105,3727)/2 = 99,2127
        div = {d["nama"]: d for d in out["divisi"]}
        self.assertEqual(r1(div["Keuangan & Admin"]["skor"]), D("99.2"))
        kode, out = self.skor("--periode", "2026-09", "--data-kosong", "nol")
        # (40x94,444 + 30x120 + 15x0 + 15x105,263)/100 = 89,567
        self.assertEqual(r1(self.orang(out, "Tono Wijaya")["skor"]), D("89.6"))

    def test_min_bobot(self):
        # Tono hanya punya 15% bobot berdata -> di bawah min 50 -> tetap belum lengkap
        p = self.file("r.csv", "periode,orang,kpi,realisasi\n2026-09,Tono Wijaya,Kehadiran tepat waktu,100\n"
                               "2026-09,Andi Pratama,Jumlah closing,15\n")
        kode, out = self.skor("--periode", "2026-09", "--data-kosong", "bobot-ulang", realisasi=p)
        self.assertIsNone(self.orang(out, "Tono Wijaya")["skor"])

    def test_bobot_divisi(self):
        kode, out = self.skor("--periode", "2026-09", "--bobot-divisi",
                              "Sales=50,Gudang & Pengiriman=30,Keuangan & Admin=20")
        # .5x96,0724 + .3x91,7279 + .2x93,0526 = 94,1651
        self.assertEqual(r1(out["perusahaan"]["skor"]), D("94.2"))
        kode, out = self.skor("--bobot-divisi", "Sales=50,Gudang & Pengiriman=30,Keuangan & Admin=10")
        self.assertEqual(kode, 1)

    def test_orang_dan_tanpa_nama(self):
        kode, out = self.skor("--periode", "2026-09", "--orang", "joko susilo")
        self.assertEqual(out["orang"]["nama"], "Joko Susilo")
        kode, out = self.skor("--periode", "2026-09", "--tanpa-nama")
        self.assertNotIn("orang", out)
        self.assertFalse(any("Tono" in w for w in out["peringatan"]))

    def test_teks_telegram(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            K.main(["skor", "--rencana", RENCANA, "--realisasi", REALISASI, "--periode", "2026-09"])
        t = buf.getvalue()
        self.assertIn("Perusahaan: 🟡 93,6 (▲6,3 vs 2026-08) — sebagian", t)
        self.assertIn("🔴 Joko Susilo (Gudang & Pengiriman): 76,7 ▼15,1", t)
        self.assertIn("bukan peringkat", t)
        self.assertIn("bukan dasar sanksi otomatis", t)

    def test_csv_keluar(self):
        out_csv = os.path.join(self.dir, "hasil.csv")
        kode, _ = self.skor("--periode", "2026-09", "--csv-keluar", out_csv)
        with open(out_csv, encoding="utf-8-sig") as f:
            isi = f.read()
        self.assertIn("2026-09,Sales,Andi Pratama,Omzet penjualan,Rp,naik,40,150000000,162000000,108,108,43.2,hijau,102.4,hijau", isi)


class UjiValidasi(Dasar):
    KEPALA = "divisi,orang,kpi,satuan,arah,bobot,target,ambang,maks_capai\n"

    def test_bobot_bukan_100(self):
        p = self.file("p.csv", self.KEPALA + "Sales,Ani,Omzet,Rp,naik,60,100,,\nSales,Ani,Closing,deal,naik,30,10,,\n")
        kode, out = jalan("cek", "--rencana", p)
        self.assertEqual(kode, 1)
        self.assertTrue(any("berjumlah 90" in e for e in out["error"]))

    def test_bobot_pecahan(self):
        p = self.file("p.csv", self.KEPALA + "Sales,Ani,Omzet,Rp,naik,\"0,6\",100,,\nSales,Ani,Closing,deal,naik,\"0,4\",10,,\n")
        kode, out = jalan("cek", "--rencana", p)
        self.assertEqual(kode, 0, out)
        self.assertTrue(any("pecahan" in c for c in out["catatan"]))

    def test_target_nol_naik_dan_negatif(self):
        p = self.file("p.csv", self.KEPALA + "Sales,Ani,Omzet,Rp,naik,50,0,,\nSales,Ani,Closing,deal,naik,50,-5,,\n")
        kode, out = jalan("cek", "--rencana", p)
        self.assertEqual(kode, 1)
        self.assertTrue(any("target 0" in e for e in out["error"]))
        self.assertTrue(any("negatif" in e for e in out["error"]))

    def test_arah_dan_ambang_salah(self):
        p = self.file("p.csv", self.KEPALA + "Sales,Ani,Omzet,Rp,besar,50,100,,\nSales,Ani,Komplain,kali,turun,50,5,3,\n")
        kode, out = jalan("cek", "--rencana", p)
        self.assertEqual(kode, 1)
        self.assertTrue(any("arah 'besar'" in e for e in out["error"]))
        self.assertTrue(any("ambang (batas maksimal) harus >= target" in e for e in out["error"]))

    def test_satu_orang_dua_divisi(self):
        p = self.file("p.csv", self.KEPALA + "Sales,Ani,Omzet,Rp,naik,100,100,,\nGudang,Ani,Akurasi,%,naik,100,99,,\n")
        kode, out = jalan("cek", "--rencana", p)
        self.assertEqual(kode, 1)

    def test_target_nol_turun_dan_cap_khusus(self):
        p = self.file("p.csv", self.KEPALA + "Produksi,Ani,Kecelakaan kerja,kejadian,turun,50,0,,\n"
                                             "Produksi,Ani,Output,unit,naik,50,100,,150\n")
        r = self.file("r.csv", "periode,orang,kpi,realisasi\n2026-09,Ani,Kecelakaan kerja,1\n2026-09,Ani,Output,200\n")
        kode, out = self.skor(rencana=p, realisasi=r)
        ani = self.orang(out, "Ani")
        # kecelakaan 1 (target 0) -> 0; output 200/100 = 200 -> cap baris 150; skor = .5x0 + .5x150 = 75
        self.assertEqual(r1(ani["skor"]), D("75.0"))

    def test_realisasi_ganda_minus_draf_dan_salah_nama(self):
        p = self.file("p.csv", self.KEPALA + "Sales,Ani,Omzet,Rp,naik,50,100,,\nSales,Ani,Konversi,%,naik,50,20,,\n")
        r = self.file("r.csv", "periode,orang,kpi,realisasi\n2026-09,Ani,Omzet,40\n2026-09,Ani,Omzet,50\n"
                               "2026-09,Ani,Konversi,20\n")
        kode, out = self.skor(rencana=p, realisasi=r)
        self.assertEqual(kode, 1)
        self.assertIn("ganda", out["error"])
        kode, out = self.skor("--duplikat", "jumlah", rencana=p, realisasi=r)
        # omzet 40+50 = 90 -> 90%; konversi 100% -> skor 95
        self.assertEqual(r1(self.orang(out, "Ani")["skor"]), D("95.0"))
        kode, out = self.skor("--duplikat", "terakhir", rencana=p, realisasi=r)
        self.assertEqual(r1(self.orang(out, "Ani")["skor"]), D("75.0"))   # .5x50 + .5x100
        r2 = self.file("r2.csv", "periode,orang,kpi,realisasi\n2026-09,Ani,Konversi,10\n2026-09,Ani,Konversi,12\n"
                                 "2026-09,Ani,Omzet,100\n")
        kode, out = self.skor("--duplikat", "jumlah", rencana=p, realisasi=r2)
        self.assertEqual(kode, 1)                                          # persen tidak boleh dijumlah
        r3 = self.file("r3.csv", "periode,orang,kpi,realisasi,status_draf\n2026-09,Ani,Omzet,-30,\n"
                                 "2026-09,Ani,Konvrsi,20,\n2026-09,Ani,Konversi,20,PERLU KONFIRMASI\n")
        kode, out = self.skor(rencana=p, realisasi=r3)
        self.assertEqual(kode, 1)            # semua baris dilewati -> tidak ada data -> tidak kirim angka nol
        self.assertIn("Belum ada satu pun realisasi", out["error"])
        kode, out = self.skor("--izinkan-minus", rencana=p, realisasi=r3)
        self.assertEqual(kode, 0)
        ani = self.orang(out, "Ani")
        self.assertEqual(ani["kpi"][0]["capaian"], "0")                    # -30/100 -> dibatasi 0
        w = " ".join(out["peringatan"])
        self.assertIn("Mungkin maksudnya 'Konversi'", w)
        self.assertIn("PERLU KONFIRMASI", w)

    def test_kpi_divisi_dan_rencana_per_periode(self):
        p = self.file("p.csv", "periode,divisi,orang,kpi,satuan,arah,bobot,target\n"
                               ",Gudang,,Pengiriman tepat waktu,%,naik,100,95\n"
                               ",Gudang,Budi,Akurasi,%,naik,100,99\n"
                               "2026-10,Gudang,Budi,Akurasi,%,naik,100,98\n")
        r = self.file("r.csv", "periode,divisi,orang,kpi,realisasi\n2026-09,Gudang,,Pengiriman tepat waktu,76\n"
                               "2026-09,Gudang,Budi,Akurasi,99\n2026-10,Gudang,Budi,Akurasi,98\n"
                               "2026-10,Gudang,,Pengiriman tepat waktu,95\n")
        kode, out = self.skor("--periode", "2026-09", rencana=p, realisasi=r)
        g = out["divisi"][0]
        # divisi pakai KPI divisi: 76/95 = 80 (bukan rata-rata individu 100)
        self.assertEqual(g["dasar_skor"], "kpi-divisi")
        self.assertEqual(r1(g["skor"]), D("80.0"))
        self.assertEqual(r1(g["rata_individu"]), D("100.0"))
        kode, out = self.skor("--periode", "2026-10", rencana=p, realisasi=r)
        # Oktober: target khusus 98 -> 98/98 = 100; tren divisi 100 - 80 = +20
        self.assertEqual(r1(self.orang(out, "Budi")["skor"]), D("100.0"))
        self.assertEqual(r1(out["divisi"][0]["tren"]), D("20.0"))


class UjiTemplateTeksOkr(Dasar):
    def test_template_xlsx_bisa_dibaca_ulang(self):
        kode, out = jalan("template", "--tim", os.path.join(TPL, "tim-contoh.csv"), "--periode", "2026-10",
                          "--keluar", self.dir)
        self.assertEqual(kode, 0, out)
        x = os.path.join(self.dir, "rencana-kpi.xlsx")
        with zipfile.ZipFile(x) as z:
            self.assertIn("xl/worksheets/sheet2.xml", z.namelist())
        kode, out = jalan("cek", "--rencana", x)
        self.assertEqual(kode, 0, out)
        self.assertEqual(out["jumlah_kpi"], 32)
        rencana, err, _ = K.baca_rencana(x)
        dewi = [b for b in rencana if b["orang"] == "Dewi Lestari" and b["kpi"] == "Rating kepuasan"][0]
        self.assertEqual(dewi["target"], D("4.7"))
        kode, out = jalan("template", "--tim", os.path.join(TPL, "tim-contoh.csv"), "--keluar", self.dir)
        self.assertEqual(kode, 1)                                          # tidak menimpa tanpa --timpa

    def test_baca_teks_wa(self):
        kode, out = jalan("baca-teks", "--rencana", RENCANA, "--teks", os.path.join(TPL, "pesan-wa-contoh.txt"),
                          "--periode", "2026-09")
        self.assertEqual(kode, 0, out)
        got = {(d["orang"], d["kpi"]): d["realisasi"] for d in out["draf"]}
        self.assertEqual(got[("Andi Pratama", "Jumlah closing")], "14")
        self.assertEqual(got[("Andi Pratama", "Omzet penjualan")], "162000000")
        self.assertEqual(got[("Rina Wulandari", "Omzet penjualan")], "96000000")   # pengirim = Rina
        self.assertEqual(got[("Joko Susilo", "Akurasi stok")], "96")
        self.assertEqual(got[("Eko Saputra", "Paket gagal kirim")], "4")
        self.assertEqual(len(out["draf"]), 9)
        self.assertTrue(all(d["status_draf"] == "PERLU KONFIRMASI" for d in out["draf"]))
        t = self.file("t.txt", "Andi closing 12 deal, target 20\nBudi 5\n")
        kode, out = jalan("baca-teks", "--rencana", RENCANA, "--teks", t, "--periode", "2026-09")
        self.assertIn("target di chat 20 berbeda dari rencana 15", out["draf"][0]["cek"])
        self.assertEqual(out["tidak_terbaca"][0]["alasan"], "KPI tidak jelas")

    def test_rekap_log(self):
        log = os.path.join(TPL, "log-operasional-contoh.csv")
        kode, out = jalan("rekap-log", "--log", log)
        self.assertEqual(kode, 0, out)
        got = {(h["orang"], h["kpi"]): h["realisasi"] for h in out["realisasi"]}
        self.assertEqual(got[("Dewi Lestari", "Waktu respons pertama")], "8")          # (6+11+7)/3
        self.assertEqual(got[("Dewi Lestari", "Komplain selesai <=2 hari")], "75")     # 3 ya dari 4
        self.assertEqual(got[("Eko Saputra", "Pengiriman tepat waktu")], "75")         # 3 ya dari 4
        self.assertEqual(got[("Joko Susilo", "Salah kirim")], "3")                     # 1 + 2
        # mingguan: ISO minggu 37 = Senin 7 - Minggu 13 Sep 2026 -> Joko 12 Sep (2),
        # Dewi komplain 9 Sep (tidak) + 10 Sep (ya) = 1 dari 2 = 50%
        kode, out = jalan("rekap-log", "--log", log, "--per", "minggu", "--periode", "2026-W37")
        self.assertEqual([(h["orang"], h["realisasi"]) for h in out["realisasi"]],
                         [("Joko Susilo", "2"), ("Dewi Lestari", "50")])
        buruk = self.file("l.csv", "tanggal,orang,kpi,nilai,cara\n31/02/2026,Ani,X,1,jumlah\n2026-09-01,Ani,Y,mungkin,persen\n")
        kode, out = jalan("rekap-log", "--log", buruk)
        self.assertEqual(kode, 1)
        self.assertIn("tidak terbaca", out["error"])
        self.assertIn("ya/tidak", out["error"])

    def test_okr(self):
        kode, out = jalan("okr", "--okr", os.path.join(TPL, "okr-contoh.csv"), "--jalan", "0,5")
        self.assertEqual(kode, 0, out)
        sales, gudang = out["objectives"]
        # (150-120)/(180-120)=0,5 ; (45-40)/(60-40)=0,25 ; 0,8 -> rata 0,5167
        self.assertEqual([k["progres"] for k in sales["key_results"]], ["0.5", "0.25", "0.8"])
        self.assertEqual(K.bulat(D(sales["progres"]), 2), D("0.52"))
        self.assertEqual(sales["key_results"][1]["status"], "merah")    # 0,25 < 0,7 x 0,5 = 0,35
        # (93-88)/(97-88)=0,5556 ; (5-8)/(2-8)=0,5 (KR menurun) -> 0,5278
        self.assertEqual(K.bulat(D(gudang["progres"]), 4), D("0.5278"))
        p = self.file("o.csv", "objective,key_result,awal,target,sekarang,progres\nA,KR1,10,10,12,\n")
        kode, out = jalan("okr", "--okr", p)
        self.assertEqual(kode, 1)


class UjiV101(Dasar):
    """Perbaikan v1.0.1 dari HASIL-UJI v1.0.0 (S-1..S-4, R-1..R-9)."""
    NAMA = ["Andi", "Rina", "Dewi", "Budi", "Joko", "Eko", "Sari", "Tono"]

    def test_s1_tanpa_nama_tidak_bocor(self):
        for mode in ("tandai", "bobot-ulang", "nol"):
            kode, out = self.skor("--periode", "2026-09", "--tanpa-nama", "--data-kosong", mode)
            teks_json = json.dumps(out, ensure_ascii=False)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                K.main(["skor", "--rencana", RENCANA, "--realisasi", REALISASI, "--periode", "2026-09",
                        "--tanpa-nama", "--data-kosong", mode])
            for n in self.NAMA:
                self.assertNotIn(n, teks_json, (mode, n))
                self.assertNotIn(n, buf.getvalue(), (mode, n))
        kode, out = self.skor("--periode", "2026-09", "--tanpa-nama")
        div = {d["nama"]: d for d in out["divisi"]}
        self.assertEqual(div["Keuangan & Admin"]["jumlah_belum_lengkap"], 1)
        self.assertNotIn("rata_individu", div["Sales"])
        self.assertIn("(1 orang belum lengkap)", self._teks("--periode", "2026-09", "--tanpa-nama"))

    def _teks(self, *extra, rencana=RENCANA, realisasi=REALISASI):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            K.main(["skor", "--rencana", rencana, "--realisasi", realisasi] + list(extra))
        return buf.getvalue()

    def test_s2_rupiah_minus(self):
        self.assertEqual(K.angka("Rp -5.000.000"), D("-5000000"))
        self.assertEqual(K.angka("-Rp5jt"), D("-5000000"))
        self.assertEqual(K.angka("(5.000.000)"), D("-5000000"))
        self.assertEqual(K.angka("(Rp 5.000)"), D("-5000"))
        self.assertEqual(K.angka("Rp 1,2 jt"), D("1200000"))
        self.assertEqual(K.angka("Rp12rb"), D("12000"))
        p = self.file("p.csv", "divisi,orang,kpi,satuan,arah,bobot,target\nUsaha,Ani,Laba,Rp,naik,100,10000000\n")
        r = self.file("r.csv", "periode,orang,kpi,realisasi\n2026-09,Ani,Laba,Rp -5.000.000\n")
        kode, out = self.skor(rencana=p, realisasi=r)
        self.assertEqual(kode, 1)                                   # minus ditolak tanpa --izinkan-minus
        kode, out = self.skor("--izinkan-minus", rencana=p, realisasi=r)
        k = self.orang(out, "Ani")["kpi"][0]
        self.assertEqual(k["realisasi"], "-5000000")
        self.assertEqual(k["capaian"], "0")                         # -5 jt / 10 jt = -50% -> 0 (bukan +50%)
        self.assertIn("0,0% (batas bawah", self._teks("--izinkan-minus", "--orang", "Ani", rencana=p, realisasi=r))

    def test_s3_rencana_berlaku_banyak_periode(self):
        kode, out = jalan("template", "--tim", os.path.join(TPL, "tim-contoh.csv"), "--periode", "2026-10",
                          "--keluar", self.dir)
        rencana = os.path.join(self.dir, "rencana-kpi.csv")
        with open(rencana, encoding="utf-8-sig") as f:
            self.assertIn("2026-10..,", f.read())
        r = self.file("r.csv", "periode,orang,kpi,realisasi\n"
                               "2026-10,Andi Pratama,Jumlah closing,15\n2026-11,Andi Pratama,Jumlah closing,12\n"
                               "2026-12,Andi Pratama,Jumlah closing,18\n")
        kode, out = self.skor("--periode", "2026-11", "--data-kosong", "bobot-ulang", "--min-bobot", "10",
                              rencana=rencana, realisasi=r)
        self.assertEqual(kode, 0, out)
        andi = self.orang(out, "Andi Pratama")
        # 12/15 = 80 ; Oktober 15/15 = 100 -> tren -20
        self.assertEqual(r1(andi["skor"]), D("80.0"))
        self.assertEqual(r1(andi["tren"]), D("-20.0"))
        self.assertEqual(out["periode_lalu"], "2026-10")
        # sebelum masa berlaku: tidak ada rencana -> pesan menyarankan rentang
        r2 = self.file("r2.csv", "periode,orang,kpi,realisasi\n2026-09,Andi Pratama,Jumlah closing,15\n")
        kode, out = self.skor("--periode", "2026-09", rencana=rencana, realisasi=r2)
        self.assertEqual(kode, 1)
        self.assertIn("2026-10..", out["error"])
        # rentang tertutup, periode tepat menang atas rentang, rentang tumpang tindih ditolak
        p = self.file("p.csv", "periode,divisi,orang,kpi,satuan,arah,bobot,target\n"
                               "2026-10..2026-11,G,Budi,Akurasi,%,naik,100,99\n"
                               "2026-11,G,Budi,Akurasi,%,naik,100,90\n")
        r3 = self.file("r3.csv", "periode,orang,kpi,realisasi\n2026-10,Budi,Akurasi,99\n2026-11,Budi,Akurasi,90\n"
                                 "2026-12,Budi,Akurasi,90\n")
        kode, out = self.skor("--periode", "2026-11", rencana=p, realisasi=r3)
        self.assertEqual(r1(self.orang(out, "Budi")["skor"]), D("100.0"))      # target khusus 90
        kode, out = self.skor("--periode", "2026-12", rencana=p, realisasi=r3)
        self.assertEqual(kode, 1)                                             # di luar rentang
        p2 = self.file("p2.csv", "periode,divisi,orang,kpi,satuan,arah,bobot,target\n"
                                 "2026-10..,G,Budi,Akurasi,%,naik,100,99\n2026-11..,G,Budi,Akurasi,%,naik,100,90\n")
        kode, out = self.skor("--periode", "2026-11", rencana=p2, realisasi=r3)
        self.assertEqual(kode, 1)
        self.assertIn("tumpang tindih", out["error"])
        p3 = self.file("p3.csv", "periode,divisi,orang,kpi,satuan,arah,bobot,target\nOkt 2026,G,Budi,Akurasi,%,naik,100,99\n")
        kode, out = jalan("cek", "--rencana", p3)
        self.assertEqual(kode, 1)

    def test_s3_peringatan_tren_hilang(self):
        kode, out = self.skor("--periode", "2026-08")
        self.assertIn("Tren tidak dihitung: file realisasi tidak berisi periode sebelumnya (2026-07).", out["peringatan"])
        p = self.file("p.csv", "divisi,orang,kpi,satuan,arah,bobot,target\nG,Budi,Akurasi,%,naik,100,99\n")
        r = self.file("r.csv", "periode,orang,kpi,realisasi\n2026-09,Budi,Akurasi,99\n2026-11,Budi,Akurasi,90\n")
        kode, out = self.skor("--periode", "2026-11", rencana=p, realisasi=r)
        self.assertIn("Periode 2026-10 tidak ada di data; tren dibandingkan dengan 2026-09.", out["peringatan"])
        self.assertEqual(K.periode_seharusnya_lalu("2026-W01"), "2025-W52")
        self.assertEqual(K.periode_seharusnya_lalu("2027-01"), "2026-12")
        self.assertEqual(K.periode_seharusnya_lalu("2026-Q1"), "2025-Q4")

    def test_s4_baca_teks_jebakan(self):
        p = self.file("p.csv", "divisi,orang,kpi,satuan,arah,bobot,target,kata_kunci\n"
                               "Mkt,Wulan,ROAS,x,naik,50,4,roas\nMkt,Wulan,Biaya per lead,Rp,turun,50,15000,cpl\n"
                               "Toko,Fajar,Pesanan dikemas hari yang sama,%,naik,50,95,packing;dikemas\n"
                               "Toko,Fajar,Transaksi per shift,transaksi,naik,50,80,transaksi\n"
                               "Toko,Rudi,Transaksi per shift,transaksi,naik,100,80,transaksi\n")
        t = self.file("t.txt", "Wulan roas 4,4x\n"
                               "Wulan cpl Rp12rb\n"
                               "Fajar target transaksi bulan depan 80\n"
                               "Fajar besok libur 1 hari\n"
                               "Rudi bantu Fajar packing 30 dus\n"
                               "Nadia belum kirim laporan\n"
                               "Rudi belum lapor transaksi\n"
                               "Selamat pagi semua\n")
        kode, out = jalan("baca-teks", "--rencana", p, "--teks", t, "--periode", "2026-09")
        got = {(d["orang"], d["kpi"]): d for d in out["draf"]}
        self.assertEqual(got[("Wulan", "ROAS")]["realisasi"], "4.4")
        self.assertEqual(got[("Wulan", "ROAS")]["cek"], "")
        self.assertEqual(got[("Wulan", "Biaya per lead")]["realisasi"], "12000")
        packing = got[("Fajar", "Pesanan dikemas hari yang sama")]
        self.assertIn("'dus'", packing["cek"])
        self.assertIn("lebih dari satu orang", packing["cek"])
        self.assertEqual(len(out["draf"]), 3)
        alasan = {g["kutipan"]: g["alasan"] for g in out["tidak_terbaca"]}
        self.assertIn("ke depan", alasan["Fajar target transaksi bulan depan 80"])
        self.assertIn("bukan angka hasil kerja", alasan["Fajar besok libur 1 hari"])
        self.assertIn("tidak ada angka", alasan["Rudi belum lapor transaksi"])
        self.assertIn("Nadia belum kirim laporan", out["diabaikan"] + list(alasan))
        self.assertEqual(out["diabaikan"][-1], "Selamat pagi semua")
        # tidak ada baris yang hilang diam-diam
        semua = {d["_kutipan"] if "_kutipan" in d else d["catatan"][11:] for d in out["draf"]}
        self.assertEqual(len(set(alasan) | semua | set(out["diabaikan"])), 8)

    def test_low_perbaikan(self):
        # R-6: status_draf selain kosong/dikonfirmasi dilewati
        p = self.file("p.csv", "divisi,orang,kpi,satuan,arah,bobot,target\nS,Ani,Omzet,Rp,naik,50,100\n"
                               "S,Ani,Keterlambatan,hari,turun,50,2\n")
        r = self.file("r.csv", "periode,orang,kpi,realisasi,status_draf\n2026-09,Ani,Omzet,90,ditolak\n"
                               "2026-09,Ani,Omzet,100,dikonfirmasi\n2026-09,Ani,Keterlambatan,6,\n")
        kode, out = self.skor(rencana=p, realisasi=r)
        self.assertEqual(kode, 0, out)
        self.assertTrue(any("status_draf 'ditolak'" in w for w in out["peringatan"]))
        # .5x100 + .5x(2-6/2=-100 -> 0) = 50
        self.assertEqual(r1(self.orang(out, "Ani")["skor"]), D("50.0"))
        t = self._teks(rencana=p, realisasi=r)
        self.assertNotIn("-100", t)                                 # R-1: tidak ada persen minus
        self.assertIn("Keterlambatan 0,0% (batas bawah", t)
        # R-3: mode nol -> perlu perhatian menunjuk KPI kosong (0%)
        r2 = self.file("r2.csv", "periode,orang,kpi,realisasi\n2026-09,Ani,Keterlambatan,2\n")
        t = self._teks("--data-kosong", "nol", rencana=p, realisasi=r2)
        self.assertIn("perlu perhatian: Omzet tanpa data (dihitung 0,0%)", t)
        # R-2: bobot-ulang tetapi bobot berdata < min -> tetap ada peringatan
        kode, out = self.skor("--data-kosong", "bobot-ulang", "--min-bobot", "60", rencana=p, realisasi=r2)
        self.assertTrue(any("Ani belum lengkap" in w and "min-bobot" in w for w in out["peringatan"]))
        # R-5: capaian tidak wajar
        r3 = self.file("r3.csv", "periode,orang,kpi,realisasi\n2026-09,Ani,Omzet,\"0,5\"\n2026-09,Ani,Keterlambatan,2\n")
        kode, out = self.skor(rencana=p, realisasi=r3)
        self.assertTrue(any("tidak wajar" in w for w in out["peringatan"]))
        # R-7: tren capaian di 1:1 diberi label poin
        t = self._teks("--periode", "2026-09", "--orang", "Joko Susilo")
        self.assertIn("(capaian ▼66,7 poin vs 2026-08)", t)
        # R-9: pipa ditutup tidak menghasilkan traceback (ditangani di __main__)
        self.assertEqual(K.VERSI, "1.0.1")


if __name__ == "__main__":
    unittest.main(verbosity=1)
