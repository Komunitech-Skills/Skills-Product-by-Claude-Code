#!/usr/bin/env python3
"""
uji_regresi_106.py - uji regresi v1.0.6 untuk scripts/olah_masukan.py (iterasi-dari-masukan-pelanggan).

Perbaikan 1.0.6 bersifat STRUKTURAL (aturan umum, bukan daftar kalimat uji):
1. kata_positif / kata_negatif boleh berupa FRASA ("belum kelar", "pelan banget"): dicocokkan pada teks yang sudah dinormalkan lalu
   digabung jadi satu token sebelum sentimen dihitung (kata tema di dalamnya tetap terbaca). Entri yang tidak bisa dipakai (bukan teks,
   emoji saja, frasa tema berisi pemisah klausa, daftar berupa satu teks) diberi PERINGATAN - tidak diabaikan diam-diam.
2. Invarian "Perlu dibaca agent": masukan bertema yang semua temanya "netral" (tanpa keluhan/pujian/saran) dan tanpa nilai tinggi masuk
   "Perlu dibaca" (alasan "tema tanpa nada"). Akibatnya menambah kata tema tidak bisa mengeluarkan masukan bernada negatif/tak terbaca
   dari daftar baca tanpa memasukkannya ke tabel keluhan.
3. Teks tanpa bintang/NPS: "jarang + kata positif/kata kerja" = keluhan ("jarang dibersihin", "jarang dibalas"), "jarang + kata keluhan"
   = pujian ("jarang telat"); keterlambatan BERANGKA ("telat 2 jam", "molor 3 hari") = keluhan kuat; negasi eksistensial atas kata
   POSITIF ("tidak ada (satupun) yang sesuai/ramah/terang") = keluhan; "dingin" baik untuk AC/kulkas/minuman; "takut/khawatir X,
   ternyata aman/utuh" = lega (bukan keluhan); "belum + kata kerja di-" = harapan belum dipenuhi (kecuali "belum dicoba/dipakai").
4. Penyamaran: kata berulang ber-angka + akhiran ("teman2nya", "dimahal2in") bukan nomor; kata kerja berimbuhan sesudah sapaan
   ("bu lanjutkan", "mas dibantu") bukan nama.

Semua kalimat BARU buatan pembuat (bukan salinan examples/ atau HASIL-UJI*.md). Set berlabel: tests/set_berlabel_106.py
(DEV dipakai selama perbaikan; HOLDOUT dijalankan sekali sesudah aturan selesai - kegagalannya dicatat di KNOWN_GAGAL_HOLDOUT).

Jalankan (dari folder skill):
    python3 tests/uji_regresi_106.py
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
import set_berlabel_106 as data  # noqa: E402

# kegagalan HOLDOUT yang diketahui (hasil satu kali jalan sesudah aturan selesai; dicatat jujur, tidak ditambal per kalimat)
# HOLDOUT 1.0.6 (satu kali jalan): 17 keluhan -> 9 masuk tabel, 8 hanya "Perlu dibaca", 0 hilang diam-diam; tema 3/4; keluhan palsu 0/8
# (2/8 bukan-keluhan ikut "Perlu dibaca"). 1.0.5 pada set yang sama: 6 hilang, 4 palsu, tema 2/4.
KNOWN_GAGAL_HOLDOUT = {
    "stafnya tidak pernah senyum",     # 'senyum' belum kata positif: hanya masuk "Perlu dibaca" (tema tanpa nada), bukan tabel Layanan
}
# penyamaran HOLDOUT 5/6; gagal (sama dengan 1.0.5): nama huruf kecil sesudah sapaan yang DIIKUTI kata lain tidak dikenali sebagai nama
KNOWN_GAGAL_SAMAR_HOLDOUT = {
    "bu melati mohon dicek",
}


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


def ukur(set_data):
    m = dict(kel=0, kel_tabel=0, hilang=0, tema=0, tema_ok=0, bukan=0, palsu=0)
    gagal = []
    for teks, b, lab in set_data:
        item, kel, pd, _ = analisis(teks, b)
        if lab is None:
            m["bukan"] += 1
            if kel:
                m["palsu"] += 1
                gagal.append(teks)
            continue
        m["kel"] += 1
        if kel:
            m["kel_tabel"] += 1
        elif pd is None:
            m["hilang"] += 1
        m["tema"] += len(lab)
        m["tema_ok"] += len(lab & kel)
        if not lab <= kel or (not kel and pd is None):
            gagal.append(teks)
    return m, gagal


class UjiSetBerlabel106(unittest.TestCase):
    def test_dev(self):
        m, gagal = ukur(data.DEV)
        # 1.0.5 pada set ini: palsu 6/15, hilang 10/20, tema 4/9
        self.assertEqual(m["palsu"], 0, (m, gagal))
        self.assertEqual(m["hilang"], 0, (m, gagal))
        self.assertEqual(m["tema_ok"], m["tema"], (m, gagal))

    def test_holdout(self):
        m, gagal = ukur(data.HOLDOUT)
        tak_terduga = [g for g in gagal if g not in KNOWN_GAGAL_HOLDOUT]
        self.assertEqual(tak_terduga, [], ("kegagalan baru di holdout", m))

    def test_samarkan(self):
        for teks, kata, tersamar in data.SAMAR_DEV:
            self.assertEqual(kata not in om.samarkan(teks), tersamar, teks)
        for teks, kata, tersamar in data.SAMAR_HOLDOUT:
            if teks not in KNOWN_GAGAL_SAMAR_HOLDOUT:
                self.assertEqual(kata not in om.samarkan(teks), tersamar, teks)

    def test_set_lama_tidak_memburuk(self):
        # set berlabel 1.0.3 + 1.0.5 (DEV+HOLDOUT): 1.0.6 tidak boleh menambah keluhan palsu atau keluhan hilang
        s = [(t, b, l) for t, b, l in data103.KELUHAN] + [(t, b, None) for t, b in data103.BUKAN_KELUHAN] + \
            [(t, None, None) for t in data103.MIRIP_TAPI_SESUAI] + list(data105.DEV) + list(data105.HOLDOUT)
        m, _ = ukur(s)
        self.assertEqual(m["palsu"], 0, m)       # 1.0.5: 0
        self.assertEqual(m["hilang"], 0, m)      # 1.0.5: 3 hilang diam-diam
        self.assertGreaterEqual(m["tema_ok"], 91, m)


class UjiFrasaSentimen(unittest.TestCase):
    KONF = {"kata_negatif": ["belum kelar", "pelan banget"], "kata_positif": ["tidak ribet", "mahal tapi sepadan"]}

    def test_frasa_negatif_berlaku(self):
        for teks in ("servis printernya belum kelar dari minggu lalu", "suara speakernya pelan banget sesudah diservis"):
            item, kel, pd, _ = analisis(teks, None, self.KONF)
            self.assertEqual(item["sentimen"], "negatif", teks)
            self.assertTrue(kel or pd, teks)
        # tanpa frasa kustom kalimat kedua tidak terbaca negatif (bukti frasanya yang bekerja)
        self.assertNotEqual(analisis("suara speakernya pelan banget sesudah diservis")[0]["sentimen"], "negatif")

    def test_frasa_positif_berlaku(self):
        self.assertEqual(analisis("daftar membernya tidak ribet", None, self.KONF)[0]["sentimen"], "positif")
        item, kel, _, _ = analisis("mahal tapi sepadan kok", None, self.KONF)
        self.assertEqual(kel, set())
        self.assertEqual(item["sentimen"], "positif")

    def test_frasa_tidak_menyembunyikan_kata_tema(self):
        item, kel, _, _ = analisis("antrean di kasir pelan banget", None, self.KONF)
        self.assertIn("waktu_tunggu", kel)

    def test_frasa_hanya_utuh_per_kata(self):
        # "kelar" sendiri / "belum kelarin" bukan frasa "belum kelar"
        self.assertNotEqual(analisis("sudah kelar kok, cepat", None, self.KONF)[0]["sentimen"], "negatif")
        self.assertEqual(om.gabung_frasa("x belum kelarin y", {"belum_kelar": re.compile(r"(?<![a-z0-9_])belum\s+kelar(?![a-z0-9_])")}),
                         "x belum kelarin y")

    def test_frasa_ikut_dinormalkan(self):
        # slang di frasa & di teks sama-sama dinormalkan ("blm kelar" = "belum kelar")
        item, _, _, _ = analisis("laptop sy blm kelar", None, {"kata_negatif": ["blm kelar"]})
        self.assertEqual(item["sentimen"], "negatif")

    def test_entri_rusak_diberi_peringatan(self):
        _, _, _, pr = analisis("x", None, {"kata_negatif": ["😡", 5, "", "lemot"], "kata_positif": "juara"})
        teks = "\n".join(pr)
        self.assertIn("😡", teks)
        self.assertIn("5", teks)
        self.assertIn("kata_positif harus daftar", teks)
        # kata_positif berupa satu teks tetap dipakai sebagai satu entri
        self.assertEqual(analisis("rasanya juara", None, {"kata_positif": "juara"})[0]["sentimen"], "positif")

    def test_kata_tema_rusak_diberi_peringatan(self):
        konf = {"tambah_kata": {"layanan": [":)", "lambat, tapi", 7, "fast respon"]}, "tema": [{"id": "x", "kata": ["🙂"]}]}
        _, _, _, pr = analisis("x", None, konf)
        teks = "\n".join(pr)
        self.assertIn(":)", teks)
        self.assertIn("lambat, tapi", teks)
        self.assertIn("7", teks)
        self.assertIn("tema \"x\" tidak punya kata", teks)
        self.assertNotIn("fast respon", teks)

    def test_kata_tema_frasa_berlaku(self):
        _, kel, _, _ = analisis("ruang tunggu bengkel sempit dan panas", None, {"tambah_kata": {"fasilitas": ["ruang tunggu"]}})
        self.assertIn("fasilitas", kel)

    def test_tanpa_konfigurasi_tanpa_peringatan(self):
        self.assertEqual(analisis("x", None, {"kata_negatif": ["belum kelar"], "kata_positif": ["mantul"]})[3], [])


class UjiInvarianPerluDibaca(unittest.TestCase):
    def _bernada_negatif(self, item, kel, pd):
        return item["sentimen"] == "negatif" or item["nada_keluhan"] or (pd == "tanpa tema" and item["sentimen"] != "positif")

    def test_tambah_kata_tema_tidak_mengeluarkan_baris_negatif(self):
        # untuk setiap kalimat berlabel keluhan & setiap kalimat bernada negatif: tambahkan SEMUA katanya sebagai kata tema.
        # Baris yang bernada negatif/tak terbaca harus tetap di tabel keluhan ATAU "Perlu dibaca".
        semua = [t for t, _, _ in data.DEV + data.HOLDOUT + data105.DEV + data105.HOLDOUT] + [t for t, _, _ in data103.KELUHAN]
        for teks in semua:
            item, kel, pd, _ = analisis(teks)
            if not (kel or pd):
                continue
            if not self._bernada_negatif(item, kel, pd) and not kel:
                continue
            kata = [w for w in re.findall(r"[a-z]{4,}", om.normalkan(item["teks"]))]
            for tid in ("layanan", "fasilitas", "kualitas_produk"):
                item2, kel2, pd2, _ = analisis(teks, None, {"tambah_kata": {tid: kata}})
                self.assertTrue(kel2 or pd2, (teks, tid, item2))

    def test_invarian_negatif_selalu_terlihat(self):
        semua = data.DEV + data.HOLDOUT + data105.DEV + data105.HOLDOUT
        for teks, b, _ in semua:
            item, kel, pd, _ = analisis(teks, b)
            if item["sentimen"] == "negatif" or item["nada_keluhan"]:
                self.assertTrue(kel or pd, teks)

    def test_tema_tanpa_nada_masuk_perlu_dibaca(self):
        item = {"teks": "servis laptop dari tanggal 3", "bintang": None, "sentimen": "netral", "tema": {"layanan": ["netral"]},
                "nada_keluhan": False}
        self.assertEqual(om.perlu_dibaca(item), "tema tanpa nada")
        # kebalikan: bernilai tinggi, pertanyaan, atau kolom permintaan -> tidak ditandai
        self.assertIsNone(om.perlu_dibaca(dict(item, bintang=5)))
        self.assertIsNone(om.perlu_dibaca(dict(item, teks="servis laptop bisa hari ini?")))
        self.assertIsNone(om.perlu_dibaca(dict(item, peran="saran")))
        self.assertIsNone(om.perlu_dibaca(dict(item, tema={"layanan": ["pujian"]}, sentimen="positif")))

    def test_berkas_dan_cetak(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "ulasan.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write("servis HP di sini 3 minggu, ditanya jawabnya besok terus\nadmin ramah dan sabar\n")
            o = Opsi()
            konf = {"tambah_kata": {"layanan": ["servis", "ditanya"]}}
            item, tema, dibuang, meta = om.olah([p], o, konf)
            r = om.ringkas(item, tema, dibuang, o, meta)
            cetak = om.cetak_teks(r, o)
            om.buat_tema(None)
        self.assertIn("3 minggu", cetak.split("## Perlu dibaca agent")[1])
        self.assertEqual(r["perlu_dibaca"]["tema_tanpa_nada"] + r["perlu_dibaca"]["keluhan_tanpa_tabel"], 1)


class UjiTeksTanpaNilai(unittest.TestCase):
    def test_jarang(self):
        for teks, tema in (("wastafel di kafe jarang dibersihin", "kebersihan"), ("chat ke admin jarang dibales", "layanan"),
                           ("lift apartemennya jarang berfungsi", "kualitas_produk")):
            self.assertIn(tema, analisis(teks)[1], teks)
        for teks in ("penjualnya jarang slow respon", "barangnya jarang cacat, QC bagus", "jarang ada toko seramah ini",
                     "tidak jarang saya belanja di sini"):
            self.assertEqual(analisis(teks)[1], set(), teks)

    def test_telat_berangka(self):
        for teks in ("montir datang telat 2 jam walau kerjanya cepat", "pengumuman hasil molor 3 hari", "antar galon terlambat sejam"):
            item, kel, _, _ = analisis(teks)
            self.assertTrue(kel, teks)
        for teks in ("telat 15 menit karena hujan deras, maklum", "cuma telat 5 menit, masih oke", "datang 2 jam lebih cepat"):
            self.assertEqual(analisis(teks)[1], set(), teks)

    def test_negasi_atas_kata_positif(self):
        for teks in ("tidak ada satupun sepatu yang sesuai ukuran", "dari tiga kasir tidak ada yang sopan", "AC ruang rapatnya gak dingin",
                     "minumannya tidak ada yang dingin"):
            item, kel, pd, _ = analisis(teks)
            self.assertEqual(item["sentimen"], "negatif", teks)
        # kebalikan: kata masalah sesudah negasi eksistensial tetap pujian; dingin untuk makanan tetap keluhan
        for teks in ("tidak ada yang rusak satupun", "AC nya dingin banget, nyaman"):
            self.assertEqual(analisis(teks)[1], set(), teks)
        self.assertTrue(analisis("nasi kotaknya sudah dingin pas sampai")[1])

    def test_takut_ternyata_aman(self):
        for teks in ("takut piringnya pecah, ternyata aman", "sempat khawatir kurirnya nyasar, alhamdulillah sampai",
                     "deg-degan takut kebesaran, ternyata pas"):
            item, kel, _, _ = analisis(teks)
            self.assertEqual(kel, set(), teks)
            self.assertNotEqual(item["sentimen"], "negatif", teks)
        for teks in ("takut pecah, ternyata benar pecah 2", "takut telat, ternyata telat 3 jam"):
            self.assertTrue(analisis(teks)[1], teks)

    def test_belum_kata_kerja(self):
        for teks in ("keluhan saya belum ditanggapi sampai hari ini", "kerusakan pipa belum diperbaiki", "kamar belum dirapikan waktu check in"):
            item, kel, pd, _ = analisis(teks)
            self.assertTrue(kel or pd, teks)
            self.assertEqual(item["sentimen"], "negatif", teks)
        for teks in ("barangnya belum dicoba, nanti diulas", "belum dipakai, semoga awet"):
            self.assertEqual(analisis(teks)[1], set(), teks)

    def test_sindiran_setelah_n_hari(self):
        for teks in ("Mantap, refund baru cair setelah 3 minggu 👍", "Keren, dibalas setelah 4 hari 🙂"):
            item, kel, pd, _ = analisis(teks)
            self.assertTrue(kel or pd, teks)
        item, kel, pd, _ = analisis("Mantap, pesanan dikirim hari ini juga 👍")
        self.assertEqual(kel, set())
        self.assertIsNone(pd)


class UjiPenyamaran106(unittest.TestCase):
    def test_kata_berulang_berangka_bukan_nomor(self):
        for teks in ("dimarahi di depan teman2nya", "harganya ga dimahal2in", "anak2ku suka", "barang2nya rapi"):
            self.assertNotIn("[nomor]", om.samarkan(teks), teks)
        for teks in ("resi JP8827361550 belum gerak", "invoice INV20260915ABC", "kode ORDER2026XYZ"):
            self.assertIn("[nomor]", om.samarkan(teks), teks)

    def test_kata_kerja_sesudah_sapaan_bukan_nama(self):
        for teks in ("mantap bu lanjutkan", "siap mas kirimkan", "makasih kak dibantu", "oke pak diproses", "sip mbak ditunggu"):
            self.assertEqual(om.samarkan(teks), teks)

    def test_nama_tetap_disamarkan(self):
        # kebalikan: nama berawalan di-/me-/ber- atau berakhiran -in/-lah tetap nama
        for teks, nama in (("halo mas dimas", "dimas"), ("makasih kak dinda", "dinda"), ("makasih pak paimin", "paimin"),
                           ("makasih pak abdullah", "abdullah"), ("makasih bu berlian", "berlian"), ("Terima kasih Mbak Melati", "Melati")):
            self.assertNotIn(nama, om.samarkan(teks), teks)


class UjiContohTidakMemburuk(unittest.TestCase):
    def test_examples_data(self):
        dd = SKILL_DIR / "examples" / "data"
        o = Opsi()
        o.staf_list = ["Dapur", "Admin"]
        item, tema, dibuang, meta = om.olah(["%s=WhatsApp" % (dd / "chat-wa.txt"), "%s=Shopee" % (dd / "ulasan-shopee.csv"),
                                             "%s=Instagram" % (dd / "komentar-instagram.txt"), "%s=Survei" % (dd / "survei-pelanggan.csv")], o)
        r = om.ringkas(item, tema, dibuang, o, meta)
        kel = {d["id"]: d["keluhan"] for d in r["tema"] if d["keluhan"]}
        # angka tabel sama dengan 1.0.5 (tidak ada perubahan pada data contoh selain daftar "Perlu dibaca" yang bertambah 2)
        # v1.0.12: baris "Pesan ini dihapus" tanpa tanggal di chat-wa.txt tidak lagi membuang keluhan Budi 22/9 (negatif 21->22, pengiriman 9->10)
        self.assertEqual(r["sentimen"], {"positif": 23, "netral": 7, "negatif": 22})
        self.assertEqual(kel.get("pengiriman"), 10)
        self.assertEqual(r["perlu_dibaca"]["tidak_terklasifikasi"], 4)


if __name__ == "__main__":
    unittest.main(verbosity=1)
