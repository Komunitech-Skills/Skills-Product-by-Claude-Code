"""Tes pph_final.py (v1.0.4: kredit PPh 22 marketplace, PP 20/2026 tanpa batas waktu OP & PT perorangan,
hari ini/besok, subtotal proyeksi, mode data belum lengkap; v1.0.6: tampilan chat tanpa tabel). Jalankan dari folder skill:
python3 -m unittest discover -s tests -v      (atau: python3 tests/test_pph_final.py)"""
import datetime
import io
import json
import os
import random
import re
import sys
import unittest
from contextlib import redirect_stdout
from decimal import Decimal, ROUND_FLOOR

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import pph_final as p  # noqa: E402

WARUNG = ["48jt", "45jt", "52jt", "70jt", "55jt", "50jt", "53jt", "58jt", "61jt", "60jt"]
OLSHOP = ["52jt", "48,5jt", "95jt", "61jt", "58jt", "64jt", "70jt", "73jt", "66jt"]


def jalankan(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = p.main(list(argv) + ["--format", "json"])
    return kode, json.loads(buf.getvalue()) if kode == 0 else None


def teks(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = p.main(list(argv))
    return kode, buf.getvalue()


class TesHitunganDasar(unittest.TestCase):
    def test_hitungan_lama_tetap(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-09-23", "--omzet",
                           "45jt", "60jt", "80jt", "120jt", "150jt", "90jt", "70jt")
        self.assertEqual(kode, 0)
        self.assertEqual([b["pph_final"] for b in h["bulan"]][-2:], [225000, 350000])
        self.assertEqual(h["ringkasan"]["total_pph_final"], 575000)
        self.assertEqual(h["versi"], "1.0.6")

    def test_skenario_warung_batas_libur(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--tahun-terdaftar", "2021",
                           "--hari-ini", "2026-10-01", "--omzet", *WARUNG)
        self.assertEqual(kode, 0)
        okt = h["bulan"][9]
        self.assertEqual(okt["pph_final"], 260000)
        self.assertEqual(okt["setor_paling_lambat"], "2026-11-15")
        self.assertEqual(okt["setor_hari_kerja"], "2026-11-16")
        semua = " ".join(h["catatan"])
        self.assertIn("Senin 16 November 2026", semua)
        self.assertIn("PMK 81/2024 Pasal 100", semua)
        self.assertIn("tidak ada lagi batas tahun", semua)
        self.assertNotIn("TERAKHIR", semua)
        self.assertFalse(any(b["batas_setor_sudah_lewat"] for b in h["bulan"]))

    def test_geser_libur_nasional_dan_cuti(self):
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 2, 15))[0], datetime.date(2026, 2, 18))
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 8, 15))[0], datetime.date(2026, 8, 18))
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 10, 15))[0], datetime.date(2026, 10, 15))
        t, _, lengkap = p.geser_hari_kerja(datetime.date(2028, 1, 15))
        self.assertEqual(t, datetime.date(2028, 1, 17))
        self.assertFalse(lengkap)

    def test_input_rusak(self):
        self.assertEqual(jalankan("--tahun", "2026", "--tahun-terdaftar", "2030", "--omzet", "10jt")[0], 2)
        self.assertEqual(jalankan("--omzet", "abc")[0], 2)
        self.assertEqual(jalankan("--omzet", "10jt", "--pph22", "1rb", "2rb")[0], 2)
        self.assertEqual(jalankan("--omzet", "10jt", "--proyeksi-mulai", "5")[0], 2)
        self.assertEqual(jalankan("--kemungkinan", "--omzet", "10jt", "20jt")[0], 2)


class TesKreditPPh22(unittest.TestCase):
    """FAQ DJP PMK 37/2025 no. 14-15: PPh 22 marketplace = bagian pelunasan PPh final masa yang sama."""

    def setUp(self):
        kode, self.h = jalankan("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14",
                                "--omzet", *OLSHOP, "--pph22", *(["0"] * 7 + ["180rb", "165rb"]))
        self.assertEqual(kode, 0)
        self.agu, self.sep = self.h["bulan"][7], self.h["bulan"][8]

    def test_lebih_bayar(self):
        self.assertEqual(self.agu["pph_final"], 107500)
        self.assertEqual(self.agu["setor_sendiri"], 0)
        self.assertEqual(self.agu["lebih_dipungut"], 72500)
        # sudah lunas lewat PPh 22 -> tidak ditandai telat walau 15 Sep sudah lewat
        self.assertFalse(self.agu["batas_setor_sudah_lewat"])
        self.assertEqual(self.agu["status_batas"], "")

    def test_kurang_bayar(self):
        self.assertEqual(self.sep["pph_final"], 330000)
        self.assertEqual(self.sep["setor_sendiri"], 165000)
        self.assertEqual(self.sep["lebih_dipungut"], 0)
        self.assertEqual(self.sep["status_batas"], "besok")
        r = self.h["ringkasan"]
        self.assertEqual(r["total_pph_final"], 437500)
        self.assertEqual(r["total_setor_sendiri_data_nyata"], 165000)
        self.assertEqual(r["total_lebih_dipungut"], 72500)
        self.assertEqual(r["batas_setor_terdekat"]["tanggal_teks"], "Kamis 15 Oktober 2026")
        self.assertEqual(r["batas_setor_terdekat"]["jarak"], "besok")
        self.assertEqual(r["bulan_batas_setor_sudah_lewat"], [])

    def test_teks_tabel_dan_catatan(self):
        _, out = teks("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--marketplace",
                      "--omzet", *OLSHOP, "--pph22", *(["0"] * 7 + ["180rb", "165rb"]), "--tampilan", "tabel")
        self.assertIn("Hari ini (tanggal acuan hitungan): Rabu 14 Oktober 2026", out)
        self.assertIn("| lebih Rp72.500 |", out)
        self.assertIn("kurang Rp165.000 (setor sendiri)", out)
        self.assertIn("Kamis 15 Okt 2026 - BESOK", out)
        self.assertIn("FAQ DJP PMK 37/2025", out)
        self.assertIn("paling lambat Senin 31 Agustus 2026", out)
        self.assertNotIn("BELUM dikurangi", out)
        self.assertNotIn("Rp 1", out)  # format standar tanpa spasi

    def test_tanpa_pph22(self):
        kode, h = jalankan("--jenis", "badan", "--jenis-badan", "pt-perorangan", "--tahun", "2026",
                           "--hari-ini", "2026-10-14", "--omzet", "35jt", "42jt", "38jt", "50jt", "47jt", "44jt",
                           "51jt", "49jt", "53jt")
        self.assertEqual(kode, 0)
        self.assertFalse(h["mode_pph22"])
        for b in h["bulan"]:
            self.assertEqual(b["setor_sendiri"], b["pph_final"])
            self.assertEqual(b["lebih_dipungut"], 0)
        self.assertEqual(h["ringkasan"]["total_pph_final"], 2045000)
        self.assertEqual(len(h["ringkasan"]["bulan_batas_setor_sudah_lewat"]), 8)
        self.assertEqual(h["bulan"][8]["status_batas"], "besok")
        for tampilan in ("tabel", "chat"):
            _, out = teks("--jenis", "badan", "--tahun", "2026", "--hari-ini", "2026-10-14", "--omzet", "35jt",
                          "--tampilan", tampilan)
            self.assertNotIn("PPh 22 dipungut", out)
            self.assertNotIn("Dipungut marketplace", out)

    def test_bebas_tapi_dipungut(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "8",
                           "--omzet", "40jt", "--pph22", "200rb")
        self.assertEqual(h["bulan"][0]["pph_final"], 0)
        self.assertEqual(h["bulan"][0]["lebih_dipungut"], 200000)
        self.assertIn("surat pernyataan bermeterai omzet s.d. Rp500 juta", " ".join(h["catatan"]))

    def test_pembulatan_selisih_ke_bawah(self):
        self.assertEqual(p.kredit_pph22(Decimal(107500), Decimal("100000.50")), (Decimal(7499), Decimal(0)))
        self.assertEqual(p.kredit_pph22(Decimal(107500), Decimal("107500.75")), (Decimal(0), Decimal(0)))
        self.assertEqual(p.kredit_pph22(Decimal(0), Decimal(0)), (Decimal(0), Decimal(0)))

    def test_cocok_hitungan_independen_acak(self):
        rnd = random.Random(20261014)
        for _ in range(300):
            jenis = rnd.choice(["op", "badan"])
            awal = rnd.randint(1, 12)
            n = rnd.randint(1, 13 - awal)
            sebelum = rnd.choice([0, rnd.randint(0, 700) * 1000000])
            omzet = [rnd.randint(0, 250000000) for _ in range(n)]
            pph22 = [rnd.choice([0, rnd.randint(0, 900000)]) for _ in range(n)]
            argv = ["--jenis", jenis, "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", str(awal),
                    "--omzet-sebelumnya", str(sebelum), "--omzet"] + [str(o) for o in omzet] + \
                   ["--pph22"] + [str(x) for x in pph22]
            kode, h = jalankan(*argv)
            self.assertEqual(kode, 0)
            kum = sebelum
            for i, b in enumerate(h["bulan"]):
                lama, kum = kum, kum + omzet[i]
                kena = max(0, kum - max(lama, 500000000)) if jenis == "op" else omzet[i]
                pph = kena * 5 // 1000
                self.assertEqual(b["pph_final"], pph)
                self.assertEqual(b["setor_sendiri"], max(0, pph - pph22[i]))
                self.assertEqual(b["lebih_dipungut"], max(0, pph22[i] - pph))


class TesHariIniDanProyeksi(unittest.TestCase):
    def test_subtotal_proyeksi(self):
        kode, h = jalankan("--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "7",
                           "--omzet-sebelumnya", "410jt", "--omzet", "95jt", "88jt", "102jt", "100jt", "100jt", "100jt",
                           "--proyeksi-mulai", "10")
        self.assertEqual(kode, 0)
        r = h["ringkasan"]
        self.assertEqual(r["total_pph_final_data_nyata"], 975000)
        self.assertEqual(r["total_pph_final"], 2475000)
        self.assertEqual(r["rentang_data_nyata"], "Juli–September")
        self.assertEqual(r["bulan_batas_setor_sudah_lewat"], ["Juli", "Agustus"])
        self.assertTrue(h["bulan"][3]["proyeksi"])
        self.assertEqual(h["bulan"][3]["status_batas"], "")
        self.assertEqual(h["bulan"][3]["setor_hari_kerja"], "2026-11-16")
        _, out = teks("--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "7",
                      "--omzet-sebelumnya", "410jt", "--omzet", "95jt", "88jt", "102jt", "100jt", "100jt", "100jt",
                      "--proyeksi-mulai", "10", "--tampilan", "tabel")
        self.assertIn("**Subtotal data nyata (Juli–September)**", out)
        self.assertIn("**Rp975.000**", out)
        self.assertIn("Oktober (proyeksi)", out)

    def test_status_relatif(self):
        hi = datetime.date(2026, 10, 14)
        self.assertEqual(p.status_relatif(datetime.date(2026, 10, 15), hi), "besok")
        self.assertEqual(p.status_relatif(datetime.date(2026, 10, 14), hi), "hari ini")
        self.assertEqual(p.status_relatif(datetime.date(2026, 9, 15), hi), "sudah lewat")
        self.assertEqual(p.keterangan_jarak(datetime.date(2026, 11, 16), hi), "33 hari lagi")
        self.assertEqual(p.format_tgl(hi), "Rabu 14 Oktober 2026")


class TesJangkaWaktuPP20(unittest.TestCase):
    def test_op_dan_pt_perorangan_tanpa_batas(self):
        for jb, terdaftar in ((None, 2020), (None, 2015), ("pt-perorangan", 2024)):
            jenis = "op" if jb is None else "badan"
            for tahun in (2026, 2027, 2030):
                t = p.catatan_jangka_waktu(jenis, jb, tahun, terdaftar)
                self.assertIn("tidak ada lagi batas tahun", t)
                self.assertIn("Pasal 59", t)
                self.assertNotIn("TERAKHIR", t)
                self.assertNotIn("MELEWATI", t)
        self.assertIn("Pasal II angka 1 huruf a", p.catatan_jangka_waktu("op", None, 2026, 2018))
        self.assertIn("pastikan ke DJP", p.catatan_jangka_waktu("badan", "pt-perorangan", 2026, 2021))

    def test_koperasi(self):
        self.assertIn("s.d. tahun pajak 2029", p.catatan_jangka_waktu("badan", "koperasi", 2026, 2021))
        self.assertIn("s.d. tahun pajak 2029", p.catatan_jangka_waktu("badan", "koperasi", 2026, 2023))
        self.assertIn("MELEWATI", p.catatan_jangka_waktu("badan", "koperasi", 2026, 2020))
        self.assertIn("s.d. tahun pajak 2030", p.catatan_jangka_waktu("badan", "koperasi", 2028, 2027))

    def test_cv_firma_pt(self):
        self.assertIn("TERAKHIR", p.catatan_jangka_waktu("badan", "cv", 2026, 2023))
        self.assertIn("MELEWATI", p.catatan_jangka_waktu("badan", "cv", 2027, 2023))
        self.assertIn("s.d. tahun pajak 2026", p.catatan_jangka_waktu("badan", "pt", 2026, 2024))
        self.assertIn("tidak bisa memakai 0,5%", p.catatan_jangka_waktu("badan", "firma", 2027, 2027))
        self.assertNotIn("--tahun-terdaftar", p.catatan_jangka_waktu("badan", "cv", 2026, None))


class TesKemungkinan(unittest.TestCase):
    def test_satu_bulan_data_kurang(self):
        kode, h = jalankan("--kemungkinan", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "10",
                           "--omzet", "85jt")
        self.assertEqual(kode, 0)
        nilai = [(k["pph_min"], k["pph_max"]) for k in h["kemungkinan"]]
        self.assertEqual(nilai, [(0, 0), (0, 425000), (425000, 425000), (425000, 425000)])
        self.assertIn("Rp415.000.000", h["kemungkinan"][0]["kondisi"])
        self.assertEqual(h["setor_hari_kerja_teks"], "Senin 16 November 2026")
        self.assertEqual(h["jarak_batas_setor"], "33 hari lagi")

    def test_kemungkinan_dengan_pph22(self):
        kode, h = jalankan("--kemungkinan", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "2",
                           "--omzet", "50jt", "--pph22", "100rb")
        self.assertEqual(h["kemungkinan"][0]["lebih_dipungut"], 100000)
        self.assertEqual(h["kemungkinan"][-1]["setor_sendiri"], 150000)


PRA_CEK_TG = ["--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-17", "--tahun-terdaftar", "2020",
              "--marketplace", "--omzet", *OLSHOP, "--pph22", *(["0"] * 7 + ["180rb", "165rb"])]
# Contoh verifikator 1.0.6: rekap 12 bulan orang pribadi, PPh 22 tiap bulan, ditanya sesudah tahun berakhir.
REKAP_12_BULAN = ("--jenis op --tahun 2027 --hari-ini 2028-02-15 --omzet 437128000 236847000 463000000 382581000 "
                  "246000000 488740000 461000000 356000000 483702000 482302000 395666000 462000000 --pph22 1529948 "
                  "828964 3241000 956452 369000 733110 1152500 890000 725553 1688057 1384831 1155000 --marketplace "
                  "--tahun-terdaftar 2020").split()
LEBAR_BIASA = 60  # omzet bulanan < Rp1 miliar tanpa sen
LEBAR_MAKS = 70   # omzet >= Rp1 miliar dan/atau bersen
POLA_BULAN = re.compile(r"^\*\*(.+?)\*\*(?: · omzet (Rp[\d.,]+))? · PPh (Rp[\d.,]+)$")


def rp(teks):
    return Decimal(teks[2:].replace(".", "").replace(",", "."))


def frp(x, desimal=False):
    return p.format_rp(Decimal(str(x)), desimal)


class TesTampilanChat(unittest.TestCase):
    """v1.0.6 (pra-cek Telegram 17 Okt 2026: tabel 10 kolom di blok kode ~120 karakter harus digeser di ponsel).
    Blok chat: tanpa tabel & blok kode; baris data pendek (<= 60 karakter tampil untuk angka biasa, <= 70 untuk omzet
    >= Rp1 miliar/bersen) dan maks. 3 kolom; keterangan/catatan = kalimat yang dilipat otomatis oleh aplikasi chat;
    blok <= 3.800 karakter ATAU dibagi tepat sekali dengan penanda pesan (tiap bagian <= 3.800, disclaimer di bagian
    terakhir); semua angka sama dengan keluaran lengkap (JSON/tabel); kurang setor, tanggal, status, dan lebih dipungut
    per masa tetap tampil."""

    def periksa(self, argv, lebar=LEBAR_MAKS):
        kode, chat = teks(*argv)
        self.assertEqual(kode, 0)
        _, h = jalankan(*argv)
        chat = chat.rstrip("\n")
        bagian_pesan = chat.split(p.PENANDA_PESAN)
        self.assertLessEqual(len(bagian_pesan), 2, argv)
        for x in bagian_pesan:
            self.assertLessEqual(len(x.strip("\n")), p.BATAS_CHAT, argv)
        if len(bagian_pesan) == 2:
            self.assertGreater(len(chat), p.BATAS_CHAT)  # dibagi hanya bila memang terlalu panjang
            self.assertIn("**Per bulan**", bagian_pesan[0])
            self.assertTrue(bagian_pesan[1].strip("\n").startswith("**Ringkasan**"))
            self.assertIn("nasihat pajak", bagian_pesan[1])  # disclaimer di pesan terakhir
            chat = chat.replace("\n" + p.PENANDA_PESAN + "\n", "")
        self.assertNotIn("```", chat)
        self.assertNotIn("|", chat)  # tidak ada tabel Markdown (Telegram mengubahnya jadi blok kode lebar)
        chat.encode("cp1252")  # Windows: keluaran lewat pipa memakai cp1252; tidak boleh UnicodeEncodeError
        baris_semua = chat.split("\n")
        bagian, dilihat = None, []
        rows = {b["nama_bulan"]: b for b in h["bulan"]}
        urut = [b["nama_bulan"] for b in h["bulan"]]
        ket_bulan, ket_grup = {}, {}
        for i, baris in enumerate(baris_semua):
            if baris.startswith("**Per bulan**"):
                bagian = "bulan"
            elif baris.startswith("**Ringkasan**"):
                bagian = "ringkasan"
            elif baris.startswith("**Catatan penting**"):
                bagian = "catatan"
            tampil = baris.replace("**", "")
            if bagian in (None, "ringkasan") or " · " in baris:
                self.assertLessEqual(len(tampil), lebar, baris)
            if bagian == "catatan" and baris.startswith("- "):
                self.assertLessEqual(len(baris), 500, baris)  # kalimat, dilipat otomatis; cegah catatan kebablasan
            if " · " in baris and bagian == "bulan":
                self.assertLessEqual(len(baris.split(" · ")), 3, baris)
                m = POLA_BULAN.match(baris)
                self.assertIsNotNone(m, baris)
                label = m.group(1).replace(" (proyeksi)", "")
                if "–" in label:
                    a, b = label.split("–")
                    grup = urut[urut.index(a):urut.index(b) + 1]
                    for x in grup:
                        ket_grup[x] = baris_semua[i + 1]
                else:
                    grup = [label]
                    self.assertEqual(" (proyeksi)" in m.group(1), rows[label]["proyeksi"])
                    ket_bulan[label] = baris_semua[i + 1]
                dilihat += grup
                if m.group(2):
                    self.assertEqual(rp(m.group(2)), sum(Decimal(str(rows[x]["omzet"])) for x in grup), baris)
                self.assertEqual(rp(m.group(3)), sum(Decimal(str(rows[x]["pph_final"])) for x in grup), baris)
        self.assertEqual(dilihat, urut)  # setiap bulan muncul tepat sekali, berurutan
        for b in h["bulan"]:
            nama, pendek = b["nama_bulan"], p.NAMA_BULAN_PENDEK[b["bulan"] - 1]
            if b["setor_sendiri"] > 0:  # kurang setor: jumlah, tanggal hari kerja, status, geser libur
                ket = ket_bulan[nama]
                if b["pph22_dipungut"] > 0:
                    self.assertIn("kurang " + frp(b["setor_sendiri"]), ket, nama)
                else:  # tanpa PPh 22: yang disetor = PPh di baris bulan (sudah dicocokkan di atas)
                    self.assertEqual(b["setor_sendiri"], b["pph_final"], nama)
                self.assertIn(p.format_tgl_tabel(datetime.date.fromisoformat(b["setor_hari_kerja"])), ket, nama)
                if b["status_batas"]:
                    self.assertIn(b["status_batas"].upper(), ket, nama)
                if b["batas_setor_hari_libur"]:
                    self.assertIn("tgl 15 libur", ket, nama)
            elif b["lebih_dipungut"] > 0:  # lebih dipungut per masa (untuk permohonan pengembalian)
                if nama in ket_bulan:
                    self.assertIn("lebih " + frp(b["lebih_dipungut"]), ket_bulan[nama], nama)
                    self.assertIn(frp(b["pph22_dipungut"], True), ket_bulan[nama], nama)
                else:
                    self.assertIn("{} {}".format(pendek, frp(b["lebih_dipungut"])), ket_grup[nama], nama)
            elif b["pph22_dipungut"] > 0:  # lunas lewat PPh 22
                if nama in ket_bulan:
                    self.assertIn(frp(b["pph22_dipungut"], True), ket_bulan[nama], nama)
                elif "lunas lewat PPh 22" in ket_grup[nama]:
                    self.assertIn("{} {}".format(pendek, frp(b["pph22_dipungut"], True)), ket_grup[nama], nama)
        r = h["ringkasan"]
        ringkasan = chat.split("**Ringkasan**")[1].split("**Catatan penting**")[0]
        self.assertIn(frp(r["omzet_kumulatif_tahun"], True), ringkasan)
        self.assertIn(frp(r["total_pph_final"]), ringkasan)
        self.assertIn(p.format_rp(max(Decimal(4800000000) - Decimal(str(r["omzet_kumulatif_tahun"])), Decimal(0)),
                                  True), ringkasan)
        if h["mode_pph22"]:
            self.assertIn("- Kurang setor (setor sendiri){}: {}".format(
                " data nyata" if r["ada_proyeksi"] else "", frp(r["total_setor_sendiri_data_nyata"])), ringkasan)
            if r["total_lebih_dipungut"]:
                self.assertIn(frp(r["total_lebih_dipungut"]), ringkasan)
        if r["batas_setor_terdekat"]:
            self.assertIn("- Setor terdekat: " + frp(r["batas_setor_terdekat"]["setor_sendiri"]), ringkasan)
        if r["bulan_batas_setor_sudah_lewat"]:
            self.assertIn("Batas setor sudah lewat per " + h["hari_ini_teks"], chat)
        catatan = chat.split("**Catatan penting**")[1]
        self.assertIn("belum dicocokkan dengan Coretax", catatan)
        self.assertIn("PMK 81/2024 Pasal 94 & 100", catatan)
        self.assertIn("SKB 3 menteri", catatan)
        self.assertIn("penghasilan lain yang dikecualikan PP 55/2022 jo. PP 20/2026", catatan)
        if h["jenis_wp"] == "badan":
            self.assertIn("tanpa pembebasan Rp500 juta", catatan)
        if r["bulan_melewati_4_8_miliar"] and h["jenis_wp"] == "op":
            self.assertIn("PP 20/2026 Pasal 57 ayat (2) huruf e & ayat (4)", catatan)
        if any("surat pernyataan bermeterai bahwa omzet sudah melewati" in c for c in h["catatan"]):
            self.assertIn("bahwa omzet sudah melewati Rp500 juta", catatan)
        self.assertIn("nasihat pajak", chat)
        return chat, h

    def test_skenario_pracek_telegram(self):
        chat, h = self.periksa(PRA_CEK_TG, LEBAR_BIASA)
        self.assertNotIn(p.PENANDA_PESAN, chat)
        self.assertLessEqual(len(chat), 3000)  # sisa ruang untuk kalimat pembuka + 3 pertanyaan (< 4.096)
        for potongan in ("Hari ini (tanggal acuan hitungan): Sabtu 17 Oktober 2026",
                         "**Januari–Juli** · omzet Rp448.500.000 · PPh Rp0",
                         "**Agustus** · omzet Rp73.000.000 · PPh Rp107.500",
                         "yang kena pajak hanya Rp21.500.000",
                         "Dipungut marketplace Rp180.000; lebih Rp72.500 (bisa diminta kembali), tidak perlu setor",
                         "**September** · omzet Rp66.000.000 · PPh Rp330.000",
                         "Dipungut marketplace Rp165.000; kurang Rp165.000, setor sendiri paling lambat Kamis 15 Okt "
                         "2026 (SUDAH LEWAT)",
                         "- Total PPh final Januari–September: Rp437.500",
                         "- Kurang setor (setor sendiri): Rp165.000",
                         "- Lebih dipungut (bisa diminta kembali): Rp72.500",
                         "- Sisa sebelum batas Rp4,8 miliar: Rp4.212.500.000",
                         "tanpa batas tahun", "(berlaku 22 April 2026, Pasal I angka 6)",
                         "dan Anda tidak memilih tarif umum", "paling lambat Senin 31 Agustus 2026",
                         "Bila dulu pernah mengirim", "bahwa omzet sudah melewati Rp500 juta",
                         "FAQ DJP PMK 37/2025 no. 14-15", "PMK 81/2024 Pasal 94 & 100", "SKB 3 menteri"):
            self.assertIn(potongan, chat)
        self.assertNotIn("TERAKHIR", chat)
        self.assertEqual(h["ringkasan"]["total_pph_final"], 437500)

    def test_bawaan_chat_dan_tabel_tetap_ada(self):
        _, bawaan = teks(*PRA_CEK_TG)
        _, chat = teks(*PRA_CEK_TG, "--tampilan", "chat")
        _, tabel = teks(*PRA_CEK_TG, "--tampilan", "tabel")
        self.assertEqual(bawaan, chat)
        self.assertIn("| Bulan | Omzet | Omzet kumulatif |", tabel)
        self.assertIn("| Agustus | Rp73.000.000 | Rp521.500.000 | Rp21.500.000 | Rp107.500 |", tabel)
        _, h = jalankan(*PRA_CEK_TG)
        self.assertNotIn("catatan_chat", h)
        self.assertNotIn("_catatan_chat", h)

    def test_skenario_lain_dan_contoh(self):
        for argv in (
                ["--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--marketplace", "--omzet", *OLSHOP,
                 "--pph22", *(["0"] * 7 + ["180rb", "165rb"])],
                ["--jenis", "badan", "--jenis-badan", "pt-perorangan", "--tahun", "2026", "--hari-ini", "2026-10-16",
                 "--omzet", "35jt", "42jt", "38jt", "50jt", "47jt", "44jt", "51jt", "49jt", "53jt"],
                ["--tahun", "2026", "--hari-ini", "2026-10-16", "--bulan-awal", "7", "--omzet-sebelumnya", "410jt",
                 "--omzet", "95jt", "88jt", "102jt", "100jt", "100jt", "100jt", "--proyeksi-mulai", "10"],
                ["--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--omzet", "38jt", "42jt", "55jt",
                 "61jt", "70jt", "88jt", "95jt", "102jt"],
                ["--jenis", "badan", "--jenis-badan", "pt-perorangan", "--tahun", "2026", "--hari-ini", "2026-10-14",
                 "--bulan-awal", "7", "--omzet-sebelumnya", "900jt", "--omzet", "150jt", "180jt"],
                ["--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "9",
                 "--omzet-sebelumnya", "470jt", "--omzet", "75jt"],
                ["--jenis", "badan", "--jenis-badan", "koperasi", "--tahun", "2026", "--tahun-terdaftar", "2021",
                 "--hari-ini", "2026-10-14", "--omzet", "400jt", "450jt", "500jt", "420jt", "380jt", "410jt", "400jt",
                 "390jt", "450jt", "420jt", "400jt", "500jt"],
                ["--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--omzet", "200jt", "300jt"]):
            with self.subTest(argv=" ".join(argv)):
                self.periksa(argv, LEBAR_BIASA)
        chat, _ = self.periksa(["--tahun", "2026", "--hari-ini", "2026-10-16", "--bulan-awal", "7",
                                "--omzet-sebelumnya", "410jt", "--omzet", "95jt", "88jt", "102jt", "100jt", "100jt",
                                "100jt", "--proyeksi-mulai", "10"], LEBAR_BIASA)
        self.assertIn("- PPh final data nyata (Juli–September): Rp975.000", chat)
        self.assertIn("- PPh termasuk proyeksi (Juli–Desember): Rp2.475.000", chat)
        self.assertIn("Senin 16 Nov 2026 (tgl 15 libur)", chat)
        chat, _ = self.periksa(["--jenis", "badan", "--jenis-badan", "pt-perorangan", "--tahun", "2026",
                                "--hari-ini", "2026-10-14", "--omzet", "35jt"])
        self.assertIn("PT perorangan lain miliknya", chat)

    def test_terpanjang_lunas_digabung(self):
        # 12 bulan semua dipungut PPh 22, lewat Rp4,8 miliar, NPWP lama, proyeksi -> bulan lunas digabung
        chat, _ = self.periksa(["--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-12-20", "--tahun-terdaftar",
                                "2018", "--marketplace", "--omzet", "520jt", "400jt", "450jt", "480jt", "470jt",
                                "490jt", "500jt", "450jt", "480jt", "470jt", "490jt", "520jt", "--pph22", "1rb", "2,6jt",
                                "2,25jt", "2,4jt", "2,35jt", "2,45jt", "2,5jt", "2,25jt", "2,4jt", "2,35jt", "2,45jt",
                                "2,6jt", "--proyeksi-mulai", "12"])
        self.assertIn("**Maret–Oktober** · omzet Rp3.790.000.000 · PPh Rp18.950.000", chat)
        self.assertIn("Mar Rp2.250.000, Apr Rp2.400.000", chat)

    def test_rekap_12_bulan_dibagi_dua_pesan(self):
        chat, h = self.periksa(REKAP_12_BULAN)
        self.assertEqual(teks(*REKAP_12_BULAN)[1].count(p.PENANDA_PESAN), 1)
        self.assertGreater(len(teks(*REKAP_12_BULAN)[1]), p.BATAS_CHAT)
        self.assertIn("lebih Rp1.529.948", chat)  # Januari & Maret: lebih dipungut per masa tetap ada
        self.assertIn("Rp3.241.000; lebih Rp926.000", chat)
        self.assertEqual(h["ringkasan"]["total_lebih_dipungut"], 2455948)

    def test_rekap_tahunan_realistis(self):
        """Profil verifikator: 12 bulan orang pribadi, omzet Rp120-380 juta/bulan, PPh 22 30-95% dari PPh tiap
        bulan, ditanya Jan-Apr tahun berikutnya (musim SPT)."""
        rnd = random.Random(20261017)
        dibagi = 0
        for i in range(120):
            dasar = rnd.randint(120, 380)
            omzet = [int(dasar * rnd.uniform(0.7, 1.3)) * 10 ** 6 + rnd.randint(0, 999) * 1000 for _ in range(12)]
            porsi = rnd.uniform(0.3, 0.95)
            pph22 = [int(o * 0.005 * porsi * rnd.uniform(0.9, 1.1)) for o in omzet]
            argv = ["--jenis", "op", "--tahun", "2026", "--hari-ini",
                    "2027-{:02d}-{:02d}".format(rnd.randint(1, 4), rnd.randint(1, 28)), "--omzet"] + \
                [str(o) for o in omzet] + ["--pph22"] + [str(x) for x in pph22] + ["--marketplace"]
            if i % 2:
                argv += ["--tahun-terdaftar", "2019"]
            chat, _ = self.periksa(argv)
            dibagi += p.PENANDA_PESAN in teks(*argv)[1]
        self.assertLess(dibagi, 12)  # pembagian dua pesan hanya cadangan (< 10%)

    def test_acak_lebar_kolom_angka(self):
        rnd = random.Random(20261017)
        for _ in range(250):
            jenis = rnd.choice(["op", "op", "badan"])
            awal = rnd.choice([1, 1, rnd.randint(1, 12)])
            n = rnd.randint(1, 13 - awal)
            omzet = [rnd.randint(0, 250) * 1000000 + rnd.choice([0, rnd.randint(0, 999999)]) for _ in range(n)]
            if rnd.random() < 0.3:  # kurang/lebih bergantian: kasus terpanjang (tidak bisa digabung)
                pph22 = [int(o * 0.005 * (1.3 if j % 2 else 0.6)) for j, o in enumerate(omzet)]
            else:
                pph22 = [rnd.choice([0, rnd.randint(0, 1500000)]) for _ in range(n)]
            tahun = rnd.choice([2026, 2027])
            argv = ["--jenis", jenis, "--tahun", str(tahun), "--hari-ini",
                    "{}-{:02d}-{:02d}".format(tahun + rnd.choice([0, 1]), rnd.randint(1, 12), rnd.randint(1, 28)),
                    "--bulan-awal", str(awal), "--omzet-sebelumnya", str(rnd.choice([0, rnd.randint(0, 700) * 10 ** 6])),
                    "--omzet"] + [str(o) for o in omzet] + ["--pph22"] + [str(x) for x in pph22]
            if jenis == "badan":
                argv += ["--jenis-badan", rnd.choice(["pt-perorangan", "koperasi", "cv"])]
            if rnd.random() < 0.5:
                argv += ["--tahun-terdaftar", str(rnd.randint(2015, tahun))]
            if rnd.random() < 0.3 and n > 1:
                argv += ["--proyeksi-mulai", str(awal + rnd.randint(1, n - 1))]
            if rnd.random() < 0.5:
                argv += ["--marketplace"]
            self.periksa(argv)

    def test_omzet_miliar_dan_bersen(self):
        rnd = random.Random(1017)
        for _ in range(60):
            omzet = ["{},{:02d}".format(rnd.randint(30, 1500) * 10 ** 6 + rnd.randint(0, 999999), rnd.randint(0, 99))
                     for _ in range(12)]
            pph22 = ["{},37".format(rnd.randint(0, 9000000)) for _ in range(12)]
            argv = ["--jenis", rnd.choice(["op", "badan"]), "--tahun", "2027", "--hari-ini", "2027-10-20",
                    "--omzet"] + omzet + ["--pph22"] + pph22 + ["--proyeksi-mulai", "10", "--marketplace"]
            self.periksa(argv, LEBAR_MAKS)

    def test_kemungkinan_chat(self):
        for argv in (["--kemungkinan", "--tahun", "2026", "--hari-ini", "2026-10-16", "--bulan-awal", "10",
                      "--omzet", "85jt"],
                     ["--kemungkinan", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "2",
                      "--omzet", "50jt", "--pph22", "100rb"]):
            _, chat = teks(*argv)
            _, h = jalankan(*argv)
            self.assertNotIn("|", chat)
            self.assertNotIn("```", chat)
            self.assertLessEqual(len(chat), p.BATAS_CHAT)
            baris = [b for b in chat.split("\n") if b.startswith("- ") and ": **Rp" in b]
            self.assertEqual(len(baris), len(h["kemungkinan"]))
            for b, k in zip(baris, h["kemungkinan"]):
                self.assertIn(k["kondisi"], b)
                self.assertIn(p.format_rp(Decimal(k["pph_min"])), b)
                self.assertIn(p.format_rp(Decimal(k["pph_max"])), b)
            self.assertIn(p.format_tgl_tabel(datetime.date.fromisoformat(h["setor_hari_kerja"])), chat)
            self.assertIn("belum dicocokkan dengan Coretax", chat)
            chat.encode("cp1252")
        self.assertIn("Senin 16 Nov 2026 (31 hari lagi)", teks(*(["--kemungkinan", "--tahun", "2026", "--hari-ini",
                                                                  "2026-10-16", "--bulan-awal", "10", "--omzet",
                                                                  "85jt"]))[1])


if __name__ == "__main__":
    unittest.main()
