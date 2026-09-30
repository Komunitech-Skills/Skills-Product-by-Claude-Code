#!/usr/bin/env python3
"""
uji_regresi.py - uji regresi v1.0.3 untuk scripts/olah_masukan.py (iterasi-dari-masukan-pelanggan).

Fokus:
1. Jaring pengaman: TIDAK ADA keluhan yang hilang diam-diam. Setiap keluhan berlabel harus masuk tabel keluhan (tema) ATAU
   daftar "Perlu dibaca agent" - diuji lewat fungsi dan lewat jalur penuh (berkas -> olah -> ringkas -> cetak/CSV).
2. Recall per tema minimal pada set berlabel baru (tests/set_berlabel_103.py), terutama ketepatan pesanan, pengiriman, stok.
3. Tanpa keluhan palsu pada pujian/pertanyaan/saran dan kalimat yang mirip salah-kirim tetapi sesuai pesanan.
4. Normalisasi slang/singkatan/huruf berulang/angka-2.

Jalankan (dari folder skill):
    python3 tests/uji_regresi.py
Uji lama tetap: python3 scripts/uji_olah_masukan.py
"""
import contextlib
import csv
import io
import os
import pathlib
import sys
import tempfile
import unittest

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))
sys.path.insert(0, str(SKILL_DIR / "tests"))

import olah_masukan as om  # noqa: E402
import set_berlabel_103 as data  # noqa: E402

SEMUA_KELUHAN = data.KELUHAN + data.KELUHAN_2
SEMUA_BUKAN = data.BUKAN_KELUHAN + data.BUKAN_KELUHAN_2

# ambang minimal (hasil v1.0.3 saat ditulis: 100% tema berlabel; ambang diberi ruang agar perubahan kecil tetap terdeteksi)
MIN_RECALL_TEMA = {"ketepatan_pesanan": 0.9, "pengiriman": 0.9, "stok_ketersediaan": 0.9}
MIN_RECALL_TEMA_TOTAL = 0.9
MIN_RECALL_BARIS = 0.85


class Opsi:
    staf_list = []
    kolom_teks = kolom_bintang = kolom_tanggal = skala = None
    buang_teks_sama = False
    contoh = 3
    min_bulan = 5
    urutan_tanggal = None


def analisis(teks, bintang=None):
    tema, pos, neg = om.buat_tema(None)
    anonim = om.samarkan(teks)
    sent, pt = om.analisis_item(anonim, bintang, tema, pos, neg)
    item = {"teks": anonim, "bintang": bintang, "sentimen": sent, "tema": {k: sorted(v) for k, v in pt.items()}}
    return item, {k for k, v in pt.items() if "keluhan" in v}


class UjiJaringPengaman(unittest.TestCase):
    def test_setiap_keluhan_masuk_tabel_atau_perlu_dibaca(self):
        hilang = []
        for teks, b, _ in SEMUA_KELUHAN:
            item, kel = analisis(teks, b)
            if not kel and not om.perlu_dibaca(item):
                hilang.append(teks)
        self.assertEqual(hilang, [], "keluhan hilang diam-diam")

    def test_jalur_penuh_csv_teks_dan_cetak(self):
        """Semua keluhan (dengan & tanpa bintang) lewat CSV: tiap teks muncul di kutipan tabel keluhan atau di 'Perlu dibaca agent'."""
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "ulasan.csv")
            with open(p, "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Rating", "Ulasan"])
                for teks, b, _ in SEMUA_KELUHAN:
                    w.writerow([b or "", teks])
            o = Opsi()
            o.contoh = 1000
            item, tema, dibuang, meta = om.olah([p], o)
            r = om.ringkas(item, tema, dibuang, o, meta)
            cetak = om.cetak_teks(r, o)
            anon = os.path.join(d, "anon.csv")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(om.main([p, "--simpan-anonim", anon, "--contoh", "1000"]), 0)
            with open(anon, encoding="utf-8") as f:
                baris = list(csv.DictReader(f))
        self.assertEqual(len(item), len(SEMUA_KELUHAN))
        self.assertIn("Tidak terklasifikasi:", cetak)
        di_tabel = {c for t in r["tema"] for c in t["contoh_keluhan"]}
        di_baca = {x["teks"] for x in r["perlu_dibaca"]["daftar"]}
        for it in item:
            teks = om.potong(it["teks"])
            self.assertTrue(teks in di_tabel or teks in di_baca, it["teks"])
            self.assertIn(teks, cetak, "tidak tercetak: " + it["teks"])
        # CSV anonim membawa kolom keluhan_tema & perlu_dibaca; tidak ada baris dengan keduanya kosong
        self.assertIn("keluhan_tema", baris[0])
        self.assertIn("perlu_dibaca", baris[0])
        kosong = [b["teks"] for b in baris if not b["keluhan_tema"] and not b["perlu_dibaca"]]
        self.assertEqual(kosong, [])

    def test_keluhan_bernada_negatif_dicetak_semua_walau_banyak(self):
        isi = "\n".join("kecewa berat pokoknya nomor %d" % i for i in range(30)) + "\n" + "\n".join(
            "halo apa kabar nomor %d" % i for i in range(30))
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write(isi)
            o = Opsi()
            item, tema, dibuang, meta = om.olah([p], o)
            r = om.ringkas(item, tema, dibuang, o, meta)
        cetak = om.cetak_teks(r, o)
        for i in range(30):
            self.assertIn("kecewa berat pokoknya nomor %d\"" % i, cetak)
        self.assertEqual(r["perlu_dibaca"]["bernada_keluhan"], 30)
        self.assertEqual(r["perlu_dibaca"]["tidak_terklasifikasi"], 60)
        self.assertIn("+10 lainnya", cetak)   # netral tanpa tema tetap dibatasi 20

    def test_keluhan_tersirat_bertema_netral_masuk_perlu_dibaca(self):
        # tema terdeteksi tetapi tidak dihitung keluhan -> tetap harus terlihat
        item = {"teks": "kok pelayanannya sekarang begitu ya", "bintang": None, "sentimen": "netral", "tema": {"layanan": ["netral"]}}
        self.assertEqual(om.perlu_dibaca(item), "keluhan tanpa tabel")
        item = {"teks": "pelayanannya biasa", "bintang": 2, "sentimen": "negatif", "tema": {"layanan": ["netral"]}}
        self.assertEqual(om.perlu_dibaca(item), "keluhan tanpa tabel")
        item = {"teks": "pelayanannya ramah", "bintang": None, "sentimen": "positif", "tema": {"layanan": ["pujian"]}}
        self.assertIsNone(om.perlu_dibaca(item))


class UjiRecall(unittest.TestCase):
    def test_recall_per_tema_dan_baris(self):
        tp, total = {}, {}
        baris = 0
        gagal = []
        for teks, b, label in SEMUA_KELUHAN:
            _, kel = analisis(teks, b)
            baris += bool(kel)
            for t in label:
                total[t] = total.get(t, 0) + 1
                if t in kel:
                    tp[t] = tp.get(t, 0) + 1
                else:
                    gagal.append((t, teks))
        for t, minimal in MIN_RECALL_TEMA.items():
            self.assertGreaterEqual(tp.get(t, 0) / total[t], minimal, "%s %d/%d %s" % (t, tp.get(t, 0), total[t], gagal))
        self.assertGreaterEqual(sum(tp.values()) / sum(total.values()), MIN_RECALL_TEMA_TOTAL, gagal)
        self.assertGreaterEqual(baris / len(SEMUA_KELUHAN), MIN_RECALL_BARIS)
        self.assertGreaterEqual(total["ketepatan_pesanan"], 20)
        self.assertGreaterEqual(total["pengiriman"], 20)
        self.assertGreaterEqual(total["stok_ketersediaan"], 12)

    def test_tanpa_keluhan_palsu(self):
        for teks, b in SEMUA_BUKAN:
            self.assertEqual(analisis(teks, b)[1], set(), teks)
        for teks in data.MIRIP_TAPI_SESUAI:
            self.assertEqual(analisis(teks)[1], set(), teks)


class UjiNormalisasi(unittest.TestCase):
    def test_slang_dan_singkatan(self):
        kasus = {"paket blm nyampe": "belum sampai", "belom dateng": "belum datang", "abis mulu": "habis", "trus": "terus",
                 "tetep aja": "tetap saja", "salkir": "salah", "chat di-read doang": "dibaca saja", "PO nya lama": "preorder",
                 "dicancel seller": "dibatalkan", "rotinya bulukan": "berjamur", "nyampenya lama": "sampainya",
                 "gaaa enak": "tidak enak", "blmmm dikirim": "belum", "ongkos kirimnya mahal": "ongkir"}
        for teks, harap in kasus.items():
            self.assertIn(harap, om.normalkan(teks), teks)

    def test_angka_dua_dan_huruf_berulang(self):
        self.assertIn("sampai", om.normalkan("belum nyampe2"))
        _, kel = analisis("telaaaat bgttt kirimnyaaa")
        self.assertIn("pengiriman", kel)

    def test_negasi_tidak_berantai(self):
        # "belum sampai" sudah dinegasi; kata sesudahnya tidak ikut dibalik
        _, kel = analisis("paketnya belum sampai udah 6 hari")
        self.assertIn("pengiriman", kel)

    def test_datang_ke_toko_bukan_pengiriman(self):
        _, kel = analisis("udah datang jauh2 ternyata kuenya habis")
        self.assertNotIn("pengiriman", kel)
        self.assertIn("stok_ketersediaan", kel)

    def test_sampai_sekarang_bukan_pengiriman(self):
        item, kel = analisis("dana refund belum masuk sampai sekarang")
        self.assertNotIn("pengiriman", kel)
        self.assertIn("pembayaran", kel)


if __name__ == "__main__":
    unittest.main(verbosity=1)
