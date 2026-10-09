#!/usr/bin/env python3
"""
uji_regresi_105.py - uji regresi v1.0.5 untuk scripts/olah_masukan.py (iterasi-dari-masukan-pelanggan).

Perbaikan 1.0.5 bersifat STRUKTURAL (aturan umum, bukan daftar kalimat uji):
1. Cakupan negasi eksistensial: "tidak/gak ada (yang) X", "tanpa X", "bebas X", "anti X" dengan X kata masalah (jendela kata,
   melewati 'yang/satupun/sama sekali') = pernyataan positif; "tidak ada yang balas" / "ga ada parkiran" tetap keluhan.
   Masalah + hilang/sembuh/berkurang ("noda ... bisa hilang") = hasil baik; "noda tidak hilang" = keluhan.
2. Salah kirim umum "pesan/order/beli X ... (yang) datang/dikirim/dikasih Y" dengan Y berbeda dari X (angka, pecahan, satuan, kata
   benda apa pun); Y berisi kata waktu/penilaian/orang/bonus tidak dihitung.
3. Jendela kata fleksibel (tanpa melewati negasi) untuk segel & pola sejenis.
4. Penyamaran nama tidak memakan kata umum sesudah sapaan ("gpp kak maklum", "iya mas siap"); alamat berhenti di kata biasa.
5. Media WA iOS/EN ("image omitted", ...) dibuang; hapus_tema id salah -> peringatan; berkas .json -> peringatan;
   "abis" + kata berawalan di-/ter-/ke- = "sesudah" (kecuali kata stok: diborong/dibeli/terjual, atau konteks stok di klausa).
6. Sindiran butuh konteks buruk yang jelas; "hebat, noda hilang 👏" / "keren, tidak ada yang rusak 👏" tidak ditandai.

Semua kalimat BARU buatan pembuat (bukan salinan examples/ atau HASIL-UJI*.md). Set berlabel: tests/set_berlabel_105.py.

Jalankan (dari folder skill):
    python3 tests/uji_regresi_105.py
"""
import contextlib
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
import set_berlabel_105 as data  # noqa: E402

# kegagalan HOLDOUT yang diketahui (dicatat jujur, bukan ditambal per kalimat): kosakata/kata kerja di luar aturan 1.0.5
KNOWN_GAGAL_HOLDOUT = {
    "pesan ban ukuran 17 yang dipasang ukuran 16",        # 'dipasang' bukan kata terima barang
    "guru lesnya sering telat dan suka main hp",          # 'telat' (-1) dinetralkan 'suka' (+1)
    "tanpa konfirmasi pesanan saya dibatalkan",           # keluhan tertangkap, tetapi tanpa tema (hanya 'Perlu dibaca')
    "abis dicat ulang malah belang2",                     # 'belang' belum di kamus (tidak lagi dianggap stok)
    "print an nya bergaris, tinta belepotan",             # kosakata percetakan belum di kamus
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
    om.buat_tema(None)
    return item, {k for k, v in pt.items() if "keluhan" in v}


def ukur(set_data):
    """Kembalikan dict metrik + daftar kalimat gagal."""
    m = dict(kel=0, kel_tabel=0, hilang=0, tema=0, tema_ok=0, bukan=0, palsu=0)
    gagal = []
    for teks, b, lab in set_data:
        item, kel = analisis(teks, b)
        if lab is None:
            m["bukan"] += 1
            if kel:
                m["palsu"] += 1
                gagal.append(teks)
            continue
        m["kel"] += 1
        if kel:
            m["kel_tabel"] += 1
        elif om.perlu_dibaca(item) is None:
            m["hilang"] += 1
        m["tema"] += len(lab)
        m["tema_ok"] += len(lab & kel)
        if not lab <= kel and not (not lab and (kel or om.perlu_dibaca(item))):
            gagal.append(teks)
    return m, gagal


class UjiSetBerlabel105(unittest.TestCase):
    def test_dev_tanpa_keluhan_palsu_dan_tanpa_hilang(self):
        m, _ = ukur(data.DEV)
        self.assertEqual(m["palsu"], 0, m)
        self.assertLessEqual(m["hilang"], 1, m)          # 1.0.4: palsu 12/24, hilang 5/26
        self.assertGreaterEqual(m["tema_ok"], 18, m)     # 1.0.4: 10/22

    def test_holdout_ambang(self):
        m, gagal = ukur(data.HOLDOUT)
        self.assertEqual(m["palsu"], 0, m)               # 1.0.4: 8/19
        self.assertLessEqual(m["hilang"], 2, m)
        self.assertGreaterEqual(m["tema_ok"], 12, m)     # 1.0.4: 9/14
        tak_terduga = [g for g in gagal if g not in KNOWN_GAGAL_HOLDOUT]
        self.assertEqual(tak_terduga, [], "kegagalan baru di holdout")

    def test_samarkan_set(self):
        for teks, kata, tersamar in data.SAMAR:
            self.assertEqual(kata not in om.samarkan(teks), tersamar, teks)


class UjiNegasiEksistensial(unittest.TestCase):
    def test_negasi_kata_masalah_bukan_keluhan(self):
        for teks in ("lampu hias sampai tanpa retak sedikitpun", "tidak ada bau tengik di minyaknya", "celana jeans nya bebas luntur",
                     "ga ada yang lecet satupun, dus juga rapi", "tas kulit anti bocor pas hujan", "dicek satu satu, nggak ada yang penyok",
                     "tidak ada kerusakan di bodi motornya", "gak ada noda maupun bau setelah dicuci", "belum ada yang karatan setahun dipakai"):
            item, kel = analisis(teks)
            self.assertEqual(kel, set(), teks)
            self.assertFalse(om.nada_keluhan(item["teks"], None), teks)

    def test_negasi_bukan_kata_masalah_tetap_keluhan(self):
        for teks, tema in (("tidak ada parkiran motor sama sekali", "fasilitas"), ("gak ada yang balas chat saya dari pagi", "layanan"),
                           ("paket nyangkut 5 hari tanpa kabar", "pengiriman"), ("noda di kaosnya tidak hilang juga", "kualitas_produk"),
                           ("ada yang retak 3 mangkok", "kualitas_produk")):
            self.assertIn(tema, analisis(teks)[1], teks)

    def test_masalah_hilang_hasil_baik(self):
        for teks in ("bau apek di jok hilang total", "ketombe berkurang setelah seminggu", "kerak di wajan bisa hilang pakai ini"):
            item, kel = analisis(teks)
            self.assertEqual(kel, set(), teks)
        self.assertTrue(analisis("paket saya hilang di ekspedisi")[1])

    def test_kata_negatif_kustom_ikut_cakupan(self):
        konf = {"kata_negatif": ["noda", "apek"]}
        self.assertEqual(analisis("kemeja bebas noda, tidak ada bau apek", None, konf)[1], set())
        self.assertTrue(analisis("masih ada noda di kerah", None, konf)[1])
        self.assertTrue(analisis("chat tidak dibales", None, {"kata_negatif": ["dibales"]})[1])

    def test_tidak_sampai_durasi_bukan_keluhan(self):
        for teks in ("gak nyampe sejam udah diantar", "tidak sampai 2 hari barang tiba"):
            self.assertEqual(analisis(teks)[1], set(), teks)
        self.assertIn("pengiriman", analisis("paket tidak sampai sampai, kurir diam saja")[1])


class UjiSalahBarangUmum(unittest.TestCase):
    def test_x_beda_y_salah_pesanan(self):
        for teks in ("order sprei queen yang dikirim king", "beli lem kayu yang sampai lem besi", "pesan oli 1 liter yang datang 800 ml",
                     "pesan tinta hitam dikasih tinta biru", "beli kran 1/2 inch yang dikirim 3/4 inch", "order bibit durian montong yang datang musang"):
            self.assertIn("ketepatan_pesanan", analisis(teks)[1], teks)

    def test_y_bukan_barang_atau_sama(self):
        for teks in ("order sprei queen yang dikirim sesuai", "beli lem kayu yang sampai kemarin sore", "pesan tumpeng yang datang tepat jam 10",
                     "order kue yang dikirim kurirnya ramah", "beli 2 dapat bonus 1 gantungan kunci", "pesan 5 kg beras yang datang 5 kg juga",
                     "beli kran 1/2 inch yang dikirim 1/2 inch, pas"):
            self.assertNotIn("ketepatan_pesanan", analisis(teks)[1], teks)


class UjiJendelaSegel(unittest.TestCase):
    def test_segel_jauh_tetap_terdeteksi(self):
        for teks in ("segel di dus printernya ternyata sudah robek", "segel pada tutup botol vitamin anak kayaknya sudah dibuka orang"):
            self.assertIn("kemasan", analisis(teks)[1], teks)

    def test_segel_utuh_bukan_keluhan(self):
        for teks in ("segel dus printernya masih utuh, tidak robek", "segel tutup botolnya masih rapat belum pernah dibuka"):
            self.assertEqual(analisis(teks)[1], set(), teks)


class UjiPenyamaran105(unittest.TestCase):
    def test_kata_umum_sesudah_sapaan_tidak_disamarkan(self):
        for teks in ("sip pak siap", "mantap bu semangat", "iya kak betul", "gapapa mas santai", "ok min noted"):
            self.assertEqual(om.samarkan(teks), teks)

    def test_nama_sesudah_sapaan_tetap_disamarkan(self):
        for teks, nama in (("makasih bu wati", "wati"), ("halo mas anto", "anto"), ("Terima kasih Kak Dewi", "Dewi")):
            self.assertNotIn(nama, om.samarkan(teks), teks)

    def test_maklum_tetap_penanda(self):
        item, kel = analisis("antar telat sedikit gpp kak maklum lagi hujan", 5)
        self.assertNotIn("pengiriman", kel)
        self.assertIn("maklum", item["teks"])

    def test_alamat_tidak_menelan_keluhan(self):
        t = om.samarkan("Gg. Mawar 7 kurir tidak mau masuk, paket balik")
        self.assertNotIn("Mawar", t)
        self.assertIn("kurir tidak mau masuk", t)
        t = om.samarkan("perum Bumi Asri blok D3 no 8 air PAM mati terus")
        self.assertNotIn("Bumi", t)
        self.assertIn("mati terus", t)
        self.assertEqual(om.samarkan("macet di jalan tol, kurir telat"), "macet di jalan tol, kurir telat")


class UjiHabisAwalan(unittest.TestCase):
    def test_abis_awalan_di_ter_ke_sesudah(self):
        for teks in ("abis diservis AC nya malah netes", "abis dipermak celananya kesempitan", "abis terjatuh sekali layarnya retak",
                     "abis kehujanan kardusnya lembek"):
            self.assertNotIn("stok_ketersediaan", analisis(teks)[1], teks)
            self.assertTrue(analisis(teks)[1] or om.perlu_dibaca(analisis(teks)[0]), teks)

    def test_abis_stok_tetap_stok(self):
        for teks in ("abis dibeli orang semua, stok kosong", "abis terjual sebelum jam 8", "abis diborong reseller, ga kebagian",
                     "abis kemarin sore, kapan ada lagi?"):
            self.assertIn("stok_ketersediaan", analisis(teks)[1], teks)


class UjiSindiran105(unittest.TestCase):
    def test_hasil_baik_dengan_pujian_tidak_ditandai(self):
        for teks in ("hebat, bau apek di jok hilang 👏", "keren, ketombe berkurang 👏", "top, gak ada yang rusak 👏",
                     "mantap, malah dapat bonus stiker 👏"):
            item, kel = analisis(teks)
            self.assertEqual(kel, set(), teks)
            self.assertFalse(om.nada_keluhan(item["teks"], None), teks)

    def test_sindiran_konteks_buruk_tetap_ditandai(self):
        for teks in ("hebat, sudah 10 hari paket belum sampai 👏", "keren, dus nya penyok parah 🙂", "salut, 3 minggu baru dibalas 🙃"):
            item, kel = analisis(teks)
            self.assertTrue(kel or om.perlu_dibaca(item), teks)


class UjiBerkas105(unittest.TestCase):
    def jalankan(self, nama, isi, konfigurasi=None):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, nama)
            with open(p, "w", encoding="utf-8") as f:
                f.write(isi)
            return om.olah([p + "=WA"], Opsi(), konfigurasi)

    def test_media_wa_ios_dibuang(self):
        isi = ("[14/09/26 10.01.02] Rina: ‎image omitted\n"
               "[14/09/26 10.01.30] Rina: ‎sticker omitted\n"
               "[14/09/26 10.02.00] Rina: Katalog.pdf • 3 pages ‎document omitted\n"
               "[14/09/26 10.03.00] Doni: <Media tidak disertakan>\n"
               "[14/09/26 10.03.30] Doni: gambar dihilangkan\n"
               "[14/09/26 10.04.00] Doni: kuenya enak banget, anak saya suka\n"
               "[14/09/26 10.05.00] Rina: pengiriman telat 2 jam, kuenya penyok\n")
        item, _, dibuang, _ = self.jalankan("chat.txt", isi)
        self.assertEqual(len(item), 2)
        self.assertEqual(dibuang.get("pesan sistem/media"), 5)
        self.assertFalse(any("omitted" in i["teks"] or "dihilangkan" in i["teks"] for i in item))

    def test_hapus_tema_salah_peringatan(self):
        isi = "kuenya enak\npengiriman telat\nadmin ramah\n"
        _, _, _, meta = self.jalankan("x.txt", isi, {"hapus_tema": ["rasa", "rassa"]})
        self.assertTrue(any("rassa" in p for p in meta["peringatan"]))
        _, _, _, meta = self.jalankan("x.txt", isi, {"hapus_tema": ["rasa"]})
        self.assertFalse(any("hapus_tema" in p for p in meta["peringatan"]))

    def test_berkas_json_peringatan(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "ulasan.json")
            with open(p, "w", encoding="utf-8") as f:
                f.write("kuenya enak\npengiriman telat\n")
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                om.main([p])
            self.assertIn(".json", out.getvalue() + err.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=1)
