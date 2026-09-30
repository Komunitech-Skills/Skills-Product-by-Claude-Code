#!/usr/bin/env python3
"""
uji_regresi_107.py - uji regresi v1.0.7 untuk scripts/olah_masukan.py (iterasi-dari-masukan-pelanggan).

Perbaikan 1.0.7 bersifat STRUKTURAL (aturan umum, bukan daftar kalimat uji):
1. Normalisasi tidak boleh mengubah kata sah: akhiran klitik (-nya/-ku/-mu/-lah/-kah) tidak ikut dihitung panjang kata saat koreksi typo
   ('krimnya' tetap 'krimnya', 'kirinya' tetap 'kirinya'; 'dikirmnya' -> 'dikirimnya'); daftar KATA_SAH hasil pemeriksaan menyeluruh semua
   bentuk hapus-1-huruf dari kamus; jenjang sekolah 'SMP'/'SMA' bukan slang 'sampai'/'sama'.
2. Pengiriman memakai konteks: kata samar (kirim/datang/telat/sampai/molor ...) tanpa kata barang/logistik + dengan kata jasa (MC, fotografer,
   kelas, tutor, teknisi ...) atau hasil kerja (desain, mockup, laporan, file ...) -> Waktu tunggu / jadwal (terlambat) atau Layanan.
   "baru dikirim setelah N hari" = keterlambatan berangka.
3. Sindiran tanpa kata negatif: pujian di klausa pertama + penanda keterlambatan/kekurangan (baru <kata kerja>, N hari baru, akhirnya
   <kata kerja>, cuma dikasih N, sampai N jam, setelah ditagih/N hari/acara) + tanpa pujian nyata di klausa lain -> [KELUHAN?].
   Nada ini tidak bergantung tema, jadi menambah kata tema tidak bisa mengeluarkannya dari "Perlu dibaca".
4. tema.json: kata_negatif/kata_positif berisi koma/titik atau hanya angka -> PERINGATAN.
5. Penyamaran: kata sifat untuk orang sesudah sapaan ("Mas telaten") bukan nama; plat = kode wilayah Indonesia + spasi konsisten
   ("A7 III", "S23 FE", "R6 II" bukan plat).

Semua kalimat BARU buatan pembuat. Set berlabel: tests/set_berlabel_107.py (DEV dipakai selama perbaikan; HOLDOUT dijalankan sekali
sesudah aturan selesai - hasilnya dicatat di bawah).

Jalankan (dari folder skill):
    python3 tests/uji_regresi_107.py
"""
import os
import pathlib
import re
import sys
import tempfile
import unittest

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))
sys.path.insert(0, str(SKILL_DIR / "tests"))

import olah_masukan as om  # noqa: E402
import set_berlabel_103 as data103  # noqa: E402
import set_berlabel_105 as data105  # noqa: E402
import set_berlabel_106 as data106  # noqa: E402
import set_berlabel_107 as data  # noqa: E402

# HOLDOUT 1.0.7 (satu kali jalan sesudah aturan selesai): tema 13/13, sindiran 9/9, penyamaran 8/8 (1.0.6 pada set yang sama: 9/13, 7/9,
# 5/8). Catatan jujur: label holdout tema banyak yang longgar (set() = cukup tabel ATAU "Perlu dibaca"); "hasil edit video baru dikirim
# seminggu setelah acara" hanya masuk "Perlu dibaca" (tema tanpa nada), "antre sampai 2 jam cuma buat potong rambut" tertangkap tetapi
# temanya salah (rambut -> Keamanan), "nasi kotak ... datang telat" ikut Kemasan, "krim sup jamurnya" (pujian) ikut "Perlu dibaca".
KNOWN_GAGAL_HOLDOUT = set()


class Opsi:
    staf_list = []
    kolom_teks = kolom_bintang = kolom_tanggal = skala = None
    buang_teks_sama = False
    contoh = 3
    min_bulan = 5
    urutan_tanggal = None


def analisis(teks, bintang=None, konfigurasi=None):
    tema, pos, neg = om.buat_tema(konfigurasi)
    anonim = om.samarkan(teks)
    sent, pt = om.analisis_item(anonim, bintang, tema, pos, neg)
    item = {"teks": anonim, "bintang": bintang, "sentimen": sent, "tema": {k: sorted(v) for k, v in pt.items()}}
    item["nada_keluhan"] = om.nada_keluhan(anonim, bintang, pos, neg)
    peringatan = list(om.buat_tema.peringatan)
    pd = om.perlu_dibaca(item, pos, neg)
    om.buat_tema(None)
    return item, {k for k, v in pt.items() if "keluhan" in v}, pd, peringatan


def gagal_tema(set_data):
    gagal = []
    for teks, b, lab, larang in set_data:
        _, kel, pd, _ = analisis(teks, b)
        if lab is None:
            ok = not kel
        else:
            ok = lab <= kel and bool(kel or pd)
        if not ok or kel & larang:
            gagal.append(teks)
    return gagal


def gagal_sindir(set_data):
    gagal = []
    for teks, sindir in set_data:
        item, kel, pd, _ = analisis(teks)
        tertangkap = bool(kel) or bool(item["nada_keluhan"] and pd)
        if tertangkap != sindir:
            gagal.append(teks)
    return gagal


def gagal_samar(set_data):
    return [t for t, kata, harus in set_data if (kata not in om.samarkan(t)) != harus]


class UjiSetBerlabel107(unittest.TestCase):
    def test_dev(self):
        self.assertEqual(gagal_tema(data.TEMA_DEV), [])
        self.assertEqual(gagal_sindir(data.SINDIR_DEV), [])
        self.assertEqual(gagal_samar(data.SAMAR_DEV), [])

    def test_holdout(self):
        g = gagal_tema(data.TEMA_HOLDOUT) + gagal_sindir(data.SINDIR_HOLDOUT) + gagal_samar(data.SAMAR_HOLDOUT)
        self.assertEqual([x for x in g if x not in KNOWN_GAGAL_HOLDOUT], [])

    def _ukur_lama(self, s):
        m = dict(palsu=0, hilang=0, tema=0, tema_ok=0)
        for teks, b, lab in s:
            _, kel, pd, _ = analisis(teks, b)
            if lab is None:
                m["palsu"] += bool(kel)
                continue
            m["hilang"] += not kel and pd is None
            m["tema"] += len(lab)
            m["tema_ok"] += len(lab & kel)
        return m

    def test_set_lama_tidak_memburuk(self):
        s = [(t, b, l) for t, b, l in data103.KELUHAN] + [(t, b, None) for t, b in data103.BUKAN_KELUHAN] + \
            [(t, None, None) for t in data103.MIRIP_TAPI_SESUAI] + list(data105.DEV) + list(data105.HOLDOUT)
        m = self._ukur_lama(s)
        self.assertEqual((m["palsu"], m["hilang"]), (0, 0), m)
        self.assertGreaterEqual(m["tema_ok"], 91, m)     # 1.0.6: 91
        m = self._ukur_lama(list(data106.DEV) + list(data106.HOLDOUT))
        self.assertEqual((m["palsu"], m["hilang"]), (0, 0), m)
        self.assertGreaterEqual(m["tema_ok"], 12, m)     # 1.0.6: 12


class UjiNormalisasiKataSah(unittest.TestCase):
    def test_kata_sah_tidak_dikoreksi(self):
        for w in sorted(om.KATA_SAH):
            for akhir in ("", "nya", "ku", "mu", "lah"):
                self.assertEqual(om.koreksi_typo(w + akhir), w + akhir, w + akhir)

    def test_kata_kamus_berakhiran_tidak_berubah(self):
        # kata kamus/kata umum + akhiran klitik tidak boleh berubah jadi kata lain (menyeluruh, bukan contoh)
        for w in sorted((om.VOCAB | om.KATA_UMUM)):
            if w.isalpha() and len(w) >= 3:
                for akhir in ("nya", "ku", "mu"):
                    self.assertEqual(om.koreksi_typo(w + akhir), w + akhir, w + akhir)

    def test_kata_dasar_pendek_berakhiran_tidak_dikoreksi(self):
        # akar 3-5 huruf + -nya tidak pernah dikoreksi lewat huruf hilang (terlalu ambigu): krim/kiri/kaca/biru ...
        for w in ("krimnya", "kirinya", "tamannya", "lemarinya", "kardusnya", "karetnya"):
            self.assertEqual(om.koreksi_typo(w), w)

    def test_typo_sah_tetap_dikoreksi(self):
        # kebalikan: typo satu huruf pada kata panjang tetap dikenali, termasuk yang berakhiran -nya
        self.assertEqual(om.koreksi_typo("pengirimn"), "pengiriman")
        self.assertEqual(om.koreksi_typo("terlmbat"), "terlambat")
        self.assertEqual(om.koreksi_typo("dibatalkn"), "dibatalkan")
        self.assertIn("pengiriman", om.normalkan("pengirimnnya lama"))

    def test_normalkan_kalimat(self):
        self.assertNotIn("kirim", om.normalkan("ada rambut di krimnya"))
        self.assertNotIn("kirim", om.normalkan("bagian kirinya penyok"))
        self.assertNotIn("sampai", om.normalkan("anak saya kelas 2 SMP"))
        self.assertNotIn("sampai", om.normalkan("les anak smp"))
        # kebalikan: slang 'smp' / 'sma' di luar konteks sekolah tetap slang
        self.assertIn("sampai", om.normalkan("udah smp rumah kak"))
        self.assertIn("sama", om.normalkan("sma kaya kemarin"))

    def test_slang_tidak_menabrak_kata_sah(self):
        # kunci SLANG tidak boleh berupa kata sah yang dilindungi, dan hasil slang tidak boleh kata sah yang berbeda arti
        self.assertEqual(set(om.SLANG) & om.KATA_SAH, set())


class UjiPengirimanKonteks(unittest.TestCase):
    def test_jasa_bukan_pengiriman(self):
        for teks, tema in (("penari tradisionalnya datang telat 1 jam ke acara", "waktu_tunggu"),
                           ("sesi konsultasi mulai terlambat 30 menit", "waktu_tunggu"),
                           ("file desain yang dikirim masih salah ejaan", None)):
            _, kel, pd, _ = analisis(teks)
            self.assertNotIn("pengiriman", kel, teks)
            self.assertTrue(kel or pd, teks)
            if tema:
                self.assertIn(tema, kel, teks)

    def test_barang_tetap_pengiriman(self):
        # kebalikan: kata barang/logistik -> tetap pengiriman walau ada kata jasa/acara
        for teks in ("paket untuk acara arisan telat 2 hari", "kirimnya telat, acaranya sudah lewat", "kurir datang telat 3 jam",
                     "produk skincare baru dikirim setelah 6 hari"):
            self.assertIn("pengiriman", analisis(teks)[1], teks)

    def test_tanpa_waktu_tunggu_tidak_error(self):
        _, kel, pd, _ = analisis("MC datang telat 1 jam", None, {"hapus_tema": ["waktu_tunggu", "layanan"]})
        self.assertNotIn("pengiriman", kel)
        self.assertTrue(kel or pd)


class UjiSindiranTanpaNilai(unittest.TestCase):
    def test_sindiran_masuk_keluhan(self):
        for teks in ("Mantap min, pesan dari pagi baru dibalas sore 👍", "hebat, 3 hari baru jawab",
                     "Keren sekali, bunga papan datang sehari setelah acaranya 👏"):
            item, kel, pd, _ = analisis(teks)
            self.assertTrue(kel or (item["nada_keluhan"] and pd), teks)

    def test_pujian_tulus_tidak_ditandai(self):
        for teks in ("Mantap, baru dicoba sekali langsung suka", "Keren, tas barunya kuat banget", "Mantap, rotinya masih lembut sampai 2 hari",
                     "Top, cuma 2 jam sudah selesai dijahit"):
            item, kel, pd, _ = analisis(teks)
            self.assertFalse(kel, teks)
            self.assertFalse(item["nada_keluhan"], teks)

    def test_tambah_kata_tema_tidak_mengeluarkan_keluhan_tanda(self):
        # invarian: untuk SETIAP baris [KELUHAN?] di semua set, tambahkan semua katanya ke beberapa tema -> tetap tabel atau [KELUHAN?]
        semua = [t for t, _ in data.SINDIR_DEV + data.SINDIR_HOLDOUT] + [t for t, _, _, _ in data.TEMA_DEV + data.TEMA_HOLDOUT] + \
                [t for t, _, _ in data106.DEV + data106.HOLDOUT + data105.DEV + data105.HOLDOUT] + [t for t, _, _ in data103.KELUHAN]
        diperiksa = 0
        for teks in semua:
            item, kel, pd, _ = analisis(teks)
            if not (item["nada_keluhan"] and pd):
                continue
            diperiksa += 1
            kata = re.findall(r"[a-z]{4,}", om.normalkan(item["teks"]))
            for tid in ("layanan", "kualitas_produk", "rasa", "fasilitas"):
                item2, kel2, pd2, _ = analisis(teks, None, {"tambah_kata": {tid: kata}})
                self.assertTrue(kel2 or (item2["nada_keluhan"] and pd2), (teks, tid))
            item3, kel3, pd3, _ = analisis(teks, None, {"tema": [{"id": "pujian_umum", "kata": kata}]})
            self.assertTrue(kel3 or (item3["nada_keluhan"] and pd3), (teks, "tema baru"))
        self.assertGreaterEqual(diperiksa, 10)

    def test_di_cetak_sebagai_keluhan(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "wa.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write("Mantap min, pesan dari pagi baru dibalas sore 👍\nadmin ramah, pengiriman cepat\n")
            o = Opsi()
            item, tema, dibuang, meta = om.olah([p], o)
            cetak = om.cetak_teks(om.ringkas(item, tema, dibuang, o, meta), o)
        self.assertRegex(cetak, r"\[KELUHAN\? [^\]]*\] \"Mantap min, pesan dari pagi baru dibalas sore")


class UjiPeringatanTemaJson107(unittest.TestCase):
    def test_koma_dan_angka(self):
        _, _, _, pr = analisis("x", None, {"kata_negatif": ["telat banget, kecewa", "123", " 45 "], "kata_positif": ["sip. mantap"]})
        teks = "\n".join(pr)
        self.assertIn("telat banget, kecewa", teks)
        self.assertIn("\"123\" hanya berisi angka", teks)
        self.assertIn("\"45\" hanya berisi angka", teks)
        self.assertIn("sip. mantap", teks)

    def test_angka_diabaikan(self):
        item, kel, _, _ = analisis("pesanan nomor 123 sudah diterima", None, {"kata_negatif": ["123"]})
        self.assertNotEqual(item["sentimen"], "negatif")

    def test_frasa_wajar_tanpa_peringatan(self):
        # kebalikan: frasa biasa, frasa ber-angka, dan 'tapi' di dalam frasa tidak diperingatkan
        _, _, _, pr = analisis("x", None, {"kata_negatif": ["telat 2 jam", "belum kelar"], "kata_positif": ["mahal tapi sepadan", "oke."]})
        self.assertEqual(pr, [])


class UjiPenyamaran107(unittest.TestCase):
    def test_sifat_sesudah_sapaan_bukan_nama(self):
        for teks in ("makasih mas telaten.", "Terima kasih Kak Sigap", "mbak gercep!", "bu teliti banget", "Makasih Pak Jujur"):
            self.assertEqual(om.samarkan(teks), teks, teks)

    def test_nama_tetap_disamarkan(self):
        for teks, nama in (("Terima kasih Mas Tegar", "Tegar"), ("makasih kak wulan.", "wulan"), ("Mas Bagas cekatan", "Bagas")):
            self.assertNotIn(nama, om.samarkan(teks), teks)

    def test_kode_produk_bukan_plat(self):
        for teks in ("sewa Sony A7 III", "Canon R5 II", "Galaxy S24 FE", "motor tipe B 125 FI", "kamera A7S", "iPhone 15 Pro"):
            self.assertNotIn("[plat]", om.samarkan(teks), teks)

    def test_plat_tetap_disamarkan(self):
        for teks in ("mobil B 1234 XYZ", "motor AB 12 CD", "plat DK1234AB", "L 3456 AB parkir"):
            s = om.samarkan(teks)
            self.assertTrue("[plat]" in s or "[nomor]" in s, teks)
            self.assertFalse(re.search(r"\d{2,}", s), teks)


class UjiContohTidakMemburuk(unittest.TestCase):
    def test_examples_data(self):
        dd = SKILL_DIR / "examples" / "data"
        o = Opsi()
        o.staf_list = ["Dapur", "Admin"]
        item, tema, dibuang, meta = om.olah(["%s=WhatsApp" % (dd / "chat-wa.txt"), "%s=Shopee" % (dd / "ulasan-shopee.csv"),
                                             "%s=Instagram" % (dd / "komentar-instagram.txt"), "%s=Survei" % (dd / "survei-pelanggan.csv")], o)
        r = om.ringkas(item, tema, dibuang, o, meta)
        kel = {d["id"]: d["keluhan"] for d in r["tema"] if d["keluhan"]}
        # sama dengan 1.0.6 (hanya label "Waktu tunggu / jadwal / antrean" yang berubah)
        self.assertEqual(r["sentimen"], {"positif": 23, "netral": 7, "negatif": 21})
        self.assertEqual(kel.get("pengiriman"), 9)
        self.assertEqual(r["perlu_dibaca"]["tidak_terklasifikasi"], 4)
        self.assertEqual(r["versi_script"], "1.0.7")


if __name__ == "__main__":
    unittest.main(verbosity=1)
