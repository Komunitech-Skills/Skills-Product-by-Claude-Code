#!/usr/bin/env python3
"""
uji_regresi_104.py - uji regresi v1.0.4 untuk scripts/olah_masukan.py (iterasi-dari-masukan-pelanggan).

Semua kalimat di sini BARU, ditulis pembuat (bukan salinan kalimat dari examples/ atau HASIL-UJI*.md). Fokus perbaikan 1.0.4:
1. "abis/habis" = sesudah/seperti ("abis minum ...", "kaya abis dibanting") bukan stok habis; stok habis tetap terdeteksi.
2. Pertanyaan restock/ready bernada senang atau bintang 4-5 = permintaan (saran), bukan keluhan stok; bernada kecewa tetap keluhan.
3. "di read"/"di-read"/"cuma dibaca" = chat diabaikan (keluhan layanan).
4. Sindiran (pujian/emoji ironi + konteks buruk) minimal masuk "Perlu dibaca agent".
5. Pertanyaan menagih ("sudah bayar ..., belum ... kak?") masuk "Perlu dibaca agent".
6. templates/tema-contoh.json tidak lagi membuat "jam makan siang" dihitung pengiriman.
Plus: "telat ..., maklum/wajar" = netral; "stok lama" = keamanan; lengket di permukaan = kebersihan, tekstur lengket bukan kebersihan.

Jalankan (dari folder skill):
    python3 tests/uji_regresi_104.py
"""
import json
import pathlib
import sys
import unittest

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import olah_masukan as om  # noqa: E402


def analisis(teks, bintang=None, konfigurasi=None):
    tema, pos, neg = om.buat_tema(konfigurasi)
    anonim = om.samarkan(teks)
    sent, pt = om.analisis_item(anonim, bintang, tema, pos, neg)
    item = {"teks": anonim, "bintang": bintang, "sentimen": sent, "tema": {k: sorted(v) for k, v in pt.items()}}
    om.buat_tema(None)   # kembalikan kata keluhan kustom ke bawaan
    return item, {k for k, v in pt.items() if "keluhan" in v}


class UjiHabisSesudah(unittest.TestCase):
    def test_abis_sesudah_bukan_stok(self):
        for teks in ("abis minum jamunya perut jadi mules", "dusnya kaya abis dibanting kurir, sudut penyok",
                     "kulit gatel2 abis 2x pake serum ini", "kyk abis ketiban lemari, kotaknya gepeng",
                     "abis dicuci sekali warnanya luntur"):
            self.assertNotIn("stok_ketersediaan", analisis(teks)[1], teks)

    def test_abis_sesudah_tetap_keluhan_tema_benar(self):
        self.assertIn("kualitas_produk", analisis("kulit gatel2 abis 2x pake serum ini")[1])
        self.assertIn("kemasan", analisis("dusnya kaya abis dibanting kurir, sudut penyok")[1])

    def test_stok_habis_tetap_terdeteksi(self):
        for teks in ("kuenya udah abis pas aku dateng jam 3", "stoknya abis terus tiap mau beli", "varian coklat abis lagi",
                     "baru buka jam 10 udah abis semua"):
            self.assertIn("stok_ketersediaan", analisis(teks)[1], teks)

    def test_stok_lama_keamanan(self):
        _, kel = analisis("kayaknya dikirimin stok lama deh, tanggalnya mepet")
        self.assertIn("keamanan", kel)
        self.assertNotIn("stok_ketersediaan", kel)


class UjiRestock(unittest.TestCase):
    def test_restock_bernada_senang_bukan_keluhan(self):
        for teks, b in (("kapan restock yg lavender kak? pengen beli lagi 🥰", 5), ("ready ukuran 42 kapan min?", 4),
                        ("kapan ready lagi yg mint? suka bgt sama rasanya", None), ("kapan ada lagi paket hampers nya? mau pesen buat kantor", None),
                        ("min kapan restock sambal cumi, favorit keluarga ❤️", 5)):
            item, kel = analisis(teks, b)
            self.assertEqual(kel, set(), teks)
            self.assertIn("saran", item["tema"].get("stok_ketersediaan", []), teks)
            self.assertIsNone(om.perlu_dibaca(item), teks)

    def test_restock_bernada_kecewa_tetap_keluhan(self):
        for teks, b in (("kapan restock? udah nunggu dari bulan kemarin", None), ("kapan ready lagi sih, kosong terus", 5),
                        ("kapan restock kak?", None), ("kapan ada lagi ukuran S", 3), ("kapan restock, dari dulu ga pernah ada 😤", None)):
            self.assertIn("stok_ketersediaan", analisis(teks, b)[1], teks)


class UjiDibaca(unittest.TestCase):
    def test_di_read_setara_diread(self):
        for teks in ("admin cuma di read aja", "chat sy di-read doang dari semalem", "pesan saya cuma diread",
                     "sudah 3x wa tapi cuma dibaca", "wa nya di read tp ga dibales"):
            self.assertIn("layanan", analisis(teks)[1], teks)

    def test_dibaca_biasa_bukan_keluhan(self):
        for teks in ("deskripsinya udah saya baca, jelas kok", "petunjuk pemakaian mudah dibaca", "label nya dibaca dulu ya kak"):
            self.assertEqual(analisis(teks)[1], set(), teks)


class UjiSindiranDanTagih(unittest.TestCase):
    def test_sindiran_minimal_perlu_dibaca(self):
        for teks in ("wow pinter bgt kurirnya, paket nyampe pas acara udah bubar 😂",
                     "top deh pelayanannya, nanya ongkir dari minggu lalu blm dijawab juga 👍",
                     "bagus ya, garansi diklaim sampe 3 minggu baru diurus 🙃",
                     "mantap tokonya, charger nya udah mati di hari kedua 👏"):
            item, kel = analisis(teks)
            self.assertTrue(kel or om.perlu_dibaca(item) == "keluhan tanpa tabel", teks)

    def test_pujian_biasa_tidak_ditandai(self):
        for teks, b in (("mantap bgt 👍 enak, pasti order lagi", 5), ("top, awet 2 minggu pakai 👍", 5),
                        ("keren, belum pernah nemu yg serapi ini 👍", 5), ("hebat, pesan jam 8 jam 9 udah nyampe 😂", None)):
            item, kel = analisis(teks, b)
            self.assertEqual(kel, set(), teks)
            self.assertFalse(om.nada_keluhan(item["teks"], b), teks)   # boleh "tanpa tema", tidak boleh [KELUHAN?]

    def test_pertanyaan_menagih_perlu_dibaca(self):
        for teks in ("udah bayar dari kemarin, statusnya blm terkonfirmasi kak?", "kenapa pesanan saya masih belum diproses?",
                     "tadi pagi sudah checkout, belum dapet nomor resi ya kak?"):
            item, kel = analisis(teks)
            self.assertTrue(kel or om.perlu_dibaca(item), teks)

    def test_pertanyaan_biasa_tidak_ditandai(self):
        for teks in ("barangnya udah ready belum kak?", "bisa kirim hari ini belum ya?", "ukuran L masih ada kak?"):
            item, kel = analisis(teks)
            self.assertEqual(kel, set(), teks)
            self.assertIsNone(om.perlu_dibaca(item), teks)


class UjiMaklumDanTema(unittest.TestCase):
    def test_telat_dimaklumi_netral(self):
        for teks, b in (("pengirimannya telat dikit krn libur panjang, maklum lah. barang bagus", 4),
                        ("kurir agak lama karena banjir, wajar kok", None), ("wajar kalo agak telat, lagi musim hujan", 5)):
            item, kel = analisis(teks, b)
            self.assertNotIn("pengiriman", kel, teks)
            self.assertNotIn("pujian", item["tema"].get("pengiriman", []), teks)
        self.assertIn("pengiriman", analisis("pengiriman telat 5 hari, ga ada kabar")[1])

    def test_tema_contoh_jam_makan_siang_bukan_pengiriman(self):
        with open(SKILL_DIR / "templates" / "tema-contoh.json", encoding="utf-8") as f:
            konf = json.load(f)
        for teks in ("ramai banget pas jam makan siang, nunggu 40 menit", "jam makan siang meja penuh semua"):
            item, _ = analisis(teks, 2, konf)
            self.assertNotIn("pengiriman", item["tema"], teks)
        self.assertIn("pengiriman", analisis("catering telat 1 jam", None, konf)[1])

    def test_lengket_permukaan_vs_tekstur(self):
        self.assertIn("kebersihan", analisis("meja nya lengket bekas kuah")[1])
        self.assertNotIn("kebersihan", analisis("serumnya lengket di muka", 3)[1])

    def test_segel_terbuka_keluhan(self):
        self.assertIn("kemasan", analisis("pas dibuka segelnya udah kebuka, ragu mau dipakai")[1])


if __name__ == "__main__":
    unittest.main(verbosity=1)
