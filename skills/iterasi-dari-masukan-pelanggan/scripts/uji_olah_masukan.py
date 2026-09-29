#!/usr/bin/env python3
"""Uji otomatis olah_masukan.py (Python standar). Jalankan: python3 scripts/uji_olah_masukan.py"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import olah_masukan as om  # noqa: E402


class Opsi:
    staf_list = []
    kolom_teks = kolom_bintang = kolom_tanggal = skala = None
    buang_teks_sama = False
    contoh = 3
    min_bulan = 5


def tulis(dir_, nama, isi):
    p = os.path.join(dir_, nama)
    with open(p, "w", encoding="utf-8") as f:
        f.write(isi)
    return p


class UjiSamarkan(unittest.TestCase):
    def test_hp_email_tautan_akun(self):
        t = om.samarkan("Hubungi 0812-3456-7890 atau +62 857 1234 5678, email a.b@x.co.id, lihat https://x.id/p?1 @budi_s")
        for bocor in ("0812", "857", "a.b@", "https", "@budi"):
            self.assertNotIn(bocor, t)
        self.assertIn("[hp]", t)

    def test_nomor_pesanan_dan_kode(self):
        t = om.samarkan("No pesanan INV/2026/0912 dan resi JP1234567890 sudah sampai")
        self.assertNotIn("1234567890", t)
        self.assertNotIn("0912", t)

    def test_kata_pesanan_biasa_tidak_hilang(self):
        self.assertIn("salah", om.samarkan("Pesanan salah kirim"))

    def test_harga_tidak_disamarkan(self):
        self.assertIn("25.000", om.samarkan("Harganya Rp 25.000 saja"))

    def test_sapaan_nama_tapi_bukan_admin(self):
        self.assertEqual(om.samarkan("Terima kasih kak Budi"), "Terima kasih kak [nama]")
        self.assertIn("kak Admin", om.samarkan("Halo kak Admin"))

    def test_nama_pengirim(self):
        self.assertNotIn("Wulandari", om.samarkan("Kata Sari Wulandari enak", ["Sari Wulandari", "Sari"]))

    def test_alamat(self):
        self.assertNotIn("Melati", om.samarkan("Kirim ke Jl. Melati No 5, Bekasi"))


class UjiSentimenTema(unittest.TestCase):
    def setUp(self):
        self.tema, self.pos, self.neg = om.buat_tema(None)

    def hasil(self, teks, bintang=None):
        return om.analisis_item(teks, bintang, self.tema, self.pos, self.neg)

    def test_negasi(self):
        sent, t = self.hasil("rasanya tidak enak")
        self.assertEqual(sent, "negatif")
        self.assertIn("keluhan", t["rasa"])
        sent, t = self.hasil("pengiriman tidak telat")
        self.assertIn("pujian", t["pengiriman"])

    def test_klausa_campuran(self):
        sent, t = self.hasil("rasa enak banget tapi pengiriman telat")
        self.assertIn("pujian", t["rasa"])
        self.assertIn("keluhan", t["pengiriman"])
        self.assertNotIn("keluhan", t["rasa"])

    def test_slang(self):
        sent, t = self.hasil("brg gk sesuai foto, packing bgt jelek")
        self.assertIn("keluhan", t["kemasan"])

    def test_bintang_rendah_tanpa_kata_negatif(self):
        sent, t = self.hasil("pengiriman kemarin sore", bintang=1)
        self.assertEqual(sent, "negatif")
        self.assertIn("keluhan", t["pengiriman"])

    def test_saran(self):
        _, t = self.hasil("semoga ada menu vegetarian")
        self.assertIn("saran", t["varian_menu"])

    def test_tema_kustom(self):
        tema, pos, neg = om.buat_tema({"tema": [{"id": "parkir", "label": "Parkir", "kata": ["parkir"], "dampak": 2}],
                                        "kata_negatif": ["sempit"]})
        _, t = om.analisis_item("parkirnya sempit", None, tema, pos, neg)
        self.assertIn("keluhan", t["parkir"])


class UjiTanggal(unittest.TestCase):
    def test_format(self):
        self.assertEqual(om.bulan_dari("12/09/2026"), "2026-09")
        self.assertEqual(om.bulan_dari("2026-08-03"), "2026-08")
        self.assertEqual(om.bulan_dari("5 Okt 2026"), "2026-10")
        self.assertEqual(om.bulan_dari("3/1/26"), "2026-01")
        self.assertIsNone(om.bulan_dari("kemarin"))
        self.assertIsNone(om.bulan_dari(""))


class UjiBerkas(unittest.TestCase):
    def jalankan(self, spes, **kw):
        o = Opsi()
        for k, v in kw.items():
            setattr(o, k, v)
        item, tema, dibuang, _ = om.olah(spes, o)
        return item, om.ringkas(item, tema, dibuang, o), dibuang

    def test_wa_staf_sistem_media_dan_nama(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "c.txt", "[02/09/2026 09.14.05] Budi Santoso: Pesanan datang telat sekali\n"
                                   "dan nasinya dingin\n"
                                   "[02/09/2026 09.20.11] Admin Toko: Maaf ya Pak Budi Santoso\n"
                                   "[02/09/2026 09.25.11] Budi Santoso: <Media tidak disertakan>\n"
                                   "02/09/2026 09.30 - Pesan dan panggilan terenkripsi end-to-end\n"
                                   "[03/09/2026 10.00.00] Sari: Rasanya enak, Budi Santoso juga suka\n")
            item, r, dibuang = self.jalankan([p + "=WA"], staf_list=["admin"])
            self.assertEqual(len(item), 2)
            semua = " ".join(i["teks"] for i in item)
            self.assertNotIn("Budi", semua)
            self.assertIn("dingin", item[0]["teks"])  # baris lanjutan tergabung
            self.assertEqual(dibuang["pesan staf"], 1)
            self.assertGreaterEqual(dibuang["pesan sistem/media"], 1)

    def test_csv_kolom_nama_tidak_dibaca_dan_duplikat(self):
        # v1.0.1: teks sama dari pembeli BERBEDA tetap dihitung; hanya baris identik (pembeli+tanggal+nilai+teks) dibuang
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "u.csv", "Nama Pembeli,Rating,Tanggal,Ulasan\nRini Hartati,1,2026-09-01,Telat banget kurirnya\n"
                                   "Lain,1,2026-09-02,telat banget kurirnya!\nX,5,2026-09-03,Enak dan rapi\n"
                                   "X,5,2026-09-03,Enak dan rapi\n")
            item, r, dibuang = self.jalankan([p + "=Shopee"])
            self.assertEqual(len(item), 3)
            self.assertEqual(dibuang.get("duplikat (baris identik)"), 1)
            self.assertNotIn("Rini", json.dumps(r, ensure_ascii=False))
            self.assertEqual(item[0]["bintang"], 1)

    def test_csv_tanpa_kolom_teks_dikenali_untuk_survei(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "s.csv", "Tanggal,Apa yang perlu diperbaiki?\n2026-09-01,Pengiriman sering telat\n2026-09-02,Kemasan bocor\n")
            item, r, _ = self.jalankan([p + "=Survei"])
            self.assertEqual(len(item), 2)

    def test_teks_bintang_dan_data_rusak(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.txt", "5 | enak banget\n★★ nasi dingin\n\n\n??\n")
            item, r, _ = self.jalankan([p + "=IG"])
            self.assertEqual([i["bintang"] for i in item], [5, 2])
            k = tulis(d, "kosong.txt", "")
            self.assertEqual(self.jalankan([k])[0], [])

    def test_hitungan_dan_tren(self):
        with tempfile.TemporaryDirectory() as d:
            baris = ["Tanggal,Rating,Ulasan"]
            for i in range(10):
                baris.append("2026-08-%02d,1,Kurir telat parah nomor %d" % (i + 1, i))
            for i in range(10):
                baris.append("2026-09-%02d,%d,%s nomor %d" % (i + 1, 1 if i < 2 else 5, "Kurir telat parah" if i < 2 else "Enak dan rapi", i + 50))
            p = tulis(d, "t.csv", "\n".join(baris))
            item, r, _ = self.jalankan([p + "=Shopee"])
            self.assertEqual(r["total_masukan"], 20)
            peng = [t for t in r["tema"] if t["id"] == "pengiriman"][0]
            self.assertEqual(peng["keluhan"], 12)
            self.assertEqual(peng["skor"], 12 * 3)
            self.assertEqual(peng["arah_tren"], "turun")
            self.assertEqual(peng["selisih_persen_poin"], -80.0)
            self.assertEqual(r["sentimen"], {"positif": 8, "netral": 0, "negatif": 12})

    def test_tren_data_kurang(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.csv", "Tanggal,Ulasan\n2026-08-01,Kurir telat\n2026-09-01,Kurir telat lagi\n")
            _, r, _ = self.jalankan([p])
            self.assertEqual(r["tema"][0]["arah_tren"], "data kurang")

    def test_cli_json_dan_simpan_anonim(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.txt", "Kak Budi, pesanan telat, telp 08123456789\nEnak banget rasanya\n")
            out = os.path.join(d, "anon.csv")
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = om.main([p, "--format", "json", "--simpan-anonim", out])
            self.assertEqual(rc, 0)
            json.loads(buf.getvalue())
            with open(out, encoding="utf-8") as f:
                isi = f.read()
            self.assertNotIn("08123456789", isi)
            self.assertNotIn("Budi", isi)


# ======================================================================= regresi v1.0.1
import contextlib  # noqa: E402
import io as _io  # noqa: E402


def jalankan_cli(args):
    out, err = _io.StringIO(), _io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = om.main(args)
    return rc, out.getvalue(), err.getvalue()


def olah_berkas(nama, isi, mode="w", **kw):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, nama)
        if isinstance(isi, bytes):
            with open(p, "wb") as f:
                f.write(isi)
        else:
            with open(p, "w", encoding="utf-8") as f:
                f.write(isi)
        o = Opsi()
        for k, v in kw.items():
            setattr(o, k, v)
        item, tema, dibuang, meta = om.olah([p], o, kw.get("konfigurasi"))
        return item, om.ringkas(item, tema, dibuang, o, meta), dibuang, meta


class UjiKolom(unittest.TestCase):
    """Permintaan 1-2 & 11: pengenalan kolom ekspor marketplace/survei."""

    def kolom(self, isi):
        _, r, _, _ = olah_berkas("x.csv", isi)
        return r["sumber"][0], r

    def test_shopee_ulasan_pembeli(self):
        s, r = self.kolom("No. Pesanan,Nama Pembeli,Ulasan Pembeli,Rating,Waktu Ulasan\n"
                          "2609120ABCDE12,rina,jahitan lepas di ujung,1,12/09/2026\n2609120ABCDE13,dewi,bagus adem,5,13/09/2026\n")
        self.assertEqual(s["kolom_teks"], ["Ulasan Pembeli"])
        self.assertEqual(s["kolom_tanggal"], "Waktu Ulasan")
        self.assertEqual(s["kolom_nilai"], "Rating")
        self.assertEqual(r["total_masukan"], 2)
        self.assertNotIn("12/09/2026", json.dumps(r))

    def test_tokopedia_balasan_penjual_tidak_dibaca(self):
        s, _ = self.kolom("Nomor Invoice,Nama Produk,Rating,Ulasan,Tanggal Ulasan,Balasan Penjual\n"
                          "INV/1/2,Kaos,2,bahannya tipis banget,2026-09-01,Maaf kak kami cek\n")
        self.assertEqual(s["kolom_teks"], ["Ulasan"])

    def test_tiktok_dan_komentar_user(self):
        s, _ = self.kolom("Order ID,Username,Review Content,Star Rating,Review Time\n5771,abc,warnanya pudar,2,2026-09-02\n")
        self.assertEqual(s["kolom_teks"], ["Review Content"])
        self.assertEqual(s["kolom_nilai"], "Star Rating")
        s, _ = self.kolom("Komentar User,Isi Ulasan,Tanggal\nkirimnya lama,barang oke,2026-09-01\n")
        self.assertEqual(s["kolom_teks"], ["Komentar User", "Isi Ulasan"])

    def test_google_form_jawaban_pendek_dan_strip(self):
        isi = ("Timestamp;Nama;No HP;Beri nilai 0-10 untuk kedai kami;Apa yang perlu kami perbaiki?;Menu apa yang ingin ditambah?\n"
               "01/08/2026 08:10:11;Andi;0812 1111 2222;9;parkiran sempit;Croissant\n"
               "03/08/2026 09:12:00;Beti;;10;ga ada, pertahankan!;Oat milk\n"
               "05/08/2026 10:00:00;Caca;;4;wifi lemot bgt;-\n")
        item, r, dibuang, _ = olah_berkas("f.csv", isi)
        s = r["sumber"][0]
        self.assertEqual(s["kolom_teks"], ["Apa yang perlu kami perbaiki?", "Menu apa yang ingin ditambah?"])
        teks = [i["teks"] for i in item]
        self.assertIn("Croissant", teks)             # jawaban 1 kata dari kolom permintaan tidak dibuang
        self.assertEqual(dibuang.get("jawaban kosong ('-', 'tidak ada')"), 1)
        menu = [t for t in r["tema"] if t["id"] == "varian_menu"][0]
        self.assertEqual(menu["saran"], 2)
        self.assertEqual(menu["keluhan"], 0)
        self.assertNotIn("Andi", json.dumps(r))

    def test_tanpa_kolom_teks_gagal_dengan_daftar_kolom(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.csv", "No. Pesanan,Waktu Ulasan,Rating\n2609120ABCDE12,12/09/2026,5\n")
            rc, out, err = jalankan_cli([p])
        self.assertEqual(rc, 2)
        self.assertIn("GAGAL", err)
        for k in ("No. Pesanan", "Waktu Ulasan", "Rating"):
            self.assertIn(k, err)

    def test_kolom_paksa_berisi_tanggal_diberi_peringatan(self):
        _, r, _, _ = olah_berkas("t.csv", "Tanggal,Ulasan\n12/09/2026,enak\n13/09/2026,telat\n",
                                 kolom_teks="Tanggal", kolom_tanggal="Tanggal")
        self.assertTrue(any("tanggal/angka/kode" in p for p in r["peringatan"]))

    def test_kolom_paksa_tidak_ada(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.csv", "Ulasan\nenak sekali\n")
            rc, _, err = jalankan_cli([p, "--kolom-teks", "Komentar"])
        self.assertEqual(rc, 2)
        self.assertIn("Ulasan", err)

    def test_banyak_baris_pendek_diberi_peringatan(self):
        isi = "Ulasan\n" + "\n".join(["ok"] * 6 + ["pengiriman telat parah"])
        _, r, _, _ = olah_berkas("t.csv", isi)
        self.assertTrue(any("terlalu pendek" in p and "Ulasan" in p for p in r["peringatan"]))


class UjiSkala(unittest.TestCase):
    """Permintaan 3: skala 0-10 vs bintang 1-5."""

    def test_nilai_0_10_dari_judul_dan_nps(self):
        isi = "Beri nilai 0-10,Komentar\n10,ga ada pertahankan\n9,kopi enak\n7,biasa saja sih\n4,wifi lemot\n5,harga naik porsi sama\n"
        item, r, _, _ = olah_berkas("s.csv", isi)
        self.assertEqual(r["sumber"][0]["skala_nilai"], "0-10")
        self.assertEqual([i["sentimen"] for i in item], ["positif", "positif", "netral", "negatif", "negatif"])
        self.assertEqual(r["nps"]["promotor_9_10"], 2)
        self.assertEqual(r["nps"]["detraktor_0_6"], 2)
        self.assertEqual(r["nps"]["nps"], 0.0)
        self.assertIsNone(item[0]["bintang"])      # 10 tidak lagi dibaca sebagai bintang 1

    def test_nilai_di_atas_5_tanpa_petunjuk_judul(self):
        item, r, _, _ = olah_berkas("s.csv", "Nilai,Komentar\n8,lumayan enak\n10,mantap\n3,basi\n")
        self.assertEqual(r["sumber"][0]["skala_nilai"], "0-10")
        self.assertEqual(item[2]["sentimen"], "negatif")

    def test_skala_ragu_diberi_peringatan_dan_bisa_dipaksa(self):
        isi = "Skor,Komentar\n5,pelayanan oke\n4,enak\n2,telat\n"
        _, r, _, _ = olah_berkas("s.csv", isi)
        self.assertEqual(r["sumber"][0]["skala_nilai"], "1-5")
        self.assertTrue(any("--skala 10" in p for p in r["peringatan"]))
        item, r, _, _ = olah_berkas("s.csv", isi, skala="10")
        self.assertEqual(r["sumber"][0]["skala_nilai"], "0-10")
        self.assertEqual(item[0]["sentimen"], "negatif")   # 5 dari 10 = detraktor

    def test_bintang_1_5_tetap(self):
        item, r, _, _ = olah_berkas("s.csv", "Rating,Ulasan\n5,mantap sekali\n1,basi semua\n4.5,enak\n")
        self.assertEqual(r["sumber"][0]["skala_nilai"], "1-5")
        self.assertEqual([i["bintang"] for i in item], [5, 1, 4])
        self.assertIsNone(r["nps"])

    def test_teks_bebas_8_per_10(self):
        item, _, _, _ = olah_berkas("t.txt", "8/10 - kopi enak tapi antre lama\n2/5 - AC mati\n")
        self.assertEqual(item[0]["nilai_0_10"], 8)
        self.assertEqual(item[1]["bintang"], 2)


class UjiNegasi(unittest.TestCase):
    """Permintaan 4: 'kurang/tidak + kata positif', 'pas' = ketika, negasi atas keluhan kustom."""

    def setUp(self):
        self.tema, self.pos, self.neg = om.buat_tema(None)

    def jenis(self, teks, tema_id, bintang=None):
        _, t = om.analisis_item(teks, bintang, self.tema, self.pos, self.neg)
        return t.get(tema_id, set())

    def test_kurang_kata_positif(self):
        self.assertEqual(self.jenis("toiletnya kurang bersih", "kebersihan", 4), {"keluhan"})
        self.assertEqual(self.jenis("pelayanannya kurang ramah pas antar", "layanan"), {"keluhan"})
        self.assertEqual(self.jenis("rasanya kurang begitu enak", "rasa"), {"keluhan"})
        self.assertEqual(self.jenis("AC kurang dingin siang hari", "fasilitas"), {"keluhan"})
        self.assertNotIn("pengiriman", om.analisis_item("AC kurang dingin", None, self.tema, self.pos, self.neg)[1])

    def test_tidak_varian_slang(self):
        for neg in ("tidak", "nggak", "gak", "ga", "gk", "ngga", "enggak"):
            self.assertEqual(self.jenis("adminnya %s ramah" % neg, "layanan"), {"keluhan"}, neg)
        self.assertEqual(self.jenis("gaenak rasanya", "rasa"), {"keluhan"})
        self.assertEqual(self.jenis("pengiriman tidak telat", "pengiriman"), {"pujian"})

    def test_pas_bukan_pujian(self):
        self.assertEqual(self.jenis("jahitannya lepas pas baru dipake", "kualitas_produk"), {"keluhan"})
        self.assertEqual(self.jenis("packing plastik tipis, sobek pas nyampe", "kemasan"), {"keluhan"})
        self.assertEqual(self.jenis("pas dateng langsung dicoba", "pengiriman"), {"netral"})
        self.assertEqual(self.jenis("ukurannya pas banget di badan", "porsi_ukuran"), {"pujian"})

    def test_aksi_dinegasi_jadi_keluhan(self):
        self.assertEqual(self.jenis("chat sy ga dibales dr kemarin", "layanan"), {"keluhan"})
        self.assertEqual(self.jenis("paket sy blm dtg udh seminggu", "pengiriman"), {"keluhan"})
        self.assertEqual(self.jenis("chargernya ga berfungsi", "kualitas_produk"), {"keluhan"})

    def test_negasi_kata_keluhan_kustom_tetap_keluhan(self):
        tema, pos, neg = om.buat_tema({"tambah_kata": {"layanan": ["dibales"]}, "kata_negatif": ["dibales"]})
        _, t = om.analisis_item("chat ga dibales", None, tema, pos, neg)
        self.assertEqual(t["layanan"], {"keluhan"})
        om.buat_tema(None)

    def test_ungkapan_netral_dan_positif(self):
        _, t = om.analisis_item("kurang lebih 2 hari sampai, aman", 5, self.tema, self.pos, self.neg)
        self.assertNotIn("keluhan", t.get("pengiriman", set()))
        for teks in ("tidak ada yang kurang, semua oke", "ga ada masalah sama sekali", "ga nyesel beli disini"):
            _, t = om.analisis_item(teks, None, self.tema, self.pos, self.neg)
            self.assertFalse(any("keluhan" in j for j in t.values()), teks)

    def test_pertanyaan_bukan_pujian(self):
        j = self.jenis("warnanya sesuai foto ga? temen beli beda jauh", "kualitas_produk")
        self.assertIn("keluhan", j)
        self.assertNotIn("pujian", j)

    def test_terlalu_dan_kurang_jumlah(self):
        self.assertEqual(self.jenis("musik terlalu kencang", "fasilitas"), {"keluhan"})
        self.assertEqual(self.jenis("kak kemarin kurang 1 kaos kaki", "ketepatan_pesanan"), {"keluhan"})

    def test_typo_aman(self):
        self.assertEqual(self.jenis("pengirimn lamaa bgt", "pengiriman"), {"keluhan"})
        self.assertEqual(om.koreksi_typo("tanggal"), "tanggal")   # tidak jadi 'tanggap'
        self.assertEqual(om.koreksi_typo("benar"), "benar")
        self.assertEqual(om.koreksi_typo("berisi"), "berisi")


# Set berlabel ringkas (dari data uji independen): (teks, bintang setara, tema keluhan yang benar)
LABEL = [
    ("warna beda sama foto, aslinya lebih gelap. kecewa", 2, "kualitas_produk"),
    ("pengiriman lama bgt 6 hari baru nyampe", 3, "pengiriman"),
    ("packing cuma plastik tipis, sobek pas nyampe", 3, "kemasan"),
    ("bagus, adem, tp ukuran kekecilan buat saya", 4, "porsi_ukuran"),
    ("dikirim salah warna, pesan navy dateng hitam", 1, "ketepatan_pesanan"),
    ("kurirnya lama, udh 5 hari", 3, "pengiriman"),
    ("min kapan restock warna sage? udh nunggu lama", None, "waktu_tunggu"),
    ("halo kak?? chat sy ga dibales dr kemarin", None, "layanan"),
    ("udh sampe kak tp kardusnya penyok", None, "kemasan"),
    ("kak kok harganya naik terus sih", None, "harga"),
    ("ka warnanya sesuai foto ga? kmrn temen sy beli beda jauh", None, "kualitas_produk"),
    ("kopinya mantap, cuma parkiran sempit", 5, "fasilitas"),
    ("wifi lemot bgt, colokan kurang, ga bisa kerja lama", 1, "fasilitas"),
    ("antrian lama pas jam makan siang, kasir cuma 1", 2, "waktu_tunggu"),
    ("gula aren kemanisan", 3, "rasa"),
    ("café nyaman, musik terlalu kencang", 3, "fasilitas"),
    ("pesanan sy ketuker sama meja sebelah, nunggu 25 menit", 2, "ketepatan_pesanan"),
    ("Tempat nyaman, sayang toiletnya kurang bersih", 4, "kebersihan"),
    ("Nemu rambut di croissant. Jijik", 1, "keamanan"),
    ("AC mati, panas bgt siang2", 2, "fasilitas"),
    ("kak cucian sy kok bau apek ya, kayak ga kering sempurna", None, "bau_aroma"),
    ("kak kemarin kurang 1 kaos kaki", None, "ketepatan_pesanan"),
    ("harga per kilo naik lagi? mahal jg ya skrg", None, "harga"),
    ("kancing kemeja sy ilang 2 abis dicuci", None, "kualitas_produk"),
    ("admin lama bales, udah 1 hari", None, "layanan"),
    ("kurang bersih nih, noda kecap masih ada", None, "kebersihan"),
    ("pelayanannya kurang ramah pas antar", None, "layanan"),
]
BUKAN_KELUHAN = ["bahannya adem bgt, jahitan rapi. recomended seller", "Barang sesuai pesanan", "admin fast respon, ramah bgt",
                 "harga murah kualitas oke, bakal order lagi", "Pengiriman cepet, packing rapi pake bubble", "barista ramah, kopi enak",
                 "setrikaannya rapi bgt, wangi. langganan terus deh", "kurirnya ramah, tepat waktu", "tanpa minus, recommended",
                 "pas banget di badan", "ga pernah telat, mantap"]


class UjiRecall(unittest.TestCase):
    """Permintaan 6: recall keluhan pada set berlabel tidak boleh turun di bawah 90%, tanpa keluhan palsu."""

    def test_recall_dan_tanpa_keluhan_palsu(self):
        tema, pos, neg = om.buat_tema(None)
        kena = 0
        for teks, b, tid in LABEL:
            _, t = om.analisis_item(om.samarkan(teks), b, tema, pos, neg)
            kena += "keluhan" in t.get(tid, set())
        self.assertGreaterEqual(kena / len(LABEL), 0.9, "recall %d/%d" % (kena, len(LABEL)))
        for teks in BUKAN_KELUHAN:
            _, t = om.analisis_item(om.samarkan(teks), None, tema, pos, neg)
            self.assertFalse(any("keluhan" in j for j in t.values()), teks)


class UjiDuplikat(unittest.TestCase):
    """Permintaan 5."""

    def test_teks_sama_pembeli_berbeda_dihitung(self):
        isi = "Nama Pembeli,Rating,Ulasan\nsri,5,Barang sesuai pesanan\nnurul,5,Barang sesuai pesanan\n"
        item, r, dibuang, _ = olah_berkas("s.csv", isi)
        self.assertEqual(len(item), 2)
        self.assertFalse(dibuang)
        self.assertTrue(any("tetap dihitung" in p for p in r["peringatan"]))

    def test_pembeli_sama_pesanan_sama_dibuang(self):
        isi = "No. Pesanan,Nama Pembeli,Rating,Ulasan\nA1,sri,5,Barang oke\nA1,sri,5,Barang oke\nA2,sri,5,Barang oke\n"
        item, _, dibuang, _ = olah_berkas("s.csv", isi)
        self.assertEqual(len(item), 2)
        self.assertEqual(dibuang.get("duplikat (baris identik)"), 1)

    def test_teks_tempelan_tidak_dibuang_kecuali_diminta(self):
        isi = "roti enak\nroti basi\nroti enak\nroti enak\nroti keras\n"
        item, r, _, _ = olah_berkas("t.txt", isi)
        self.assertEqual(len(item), 5)
        rasa = [t for t in r["tema"] if t["id"] == "rasa"][0]
        self.assertEqual(rasa["pujian"], 3)
        item, _, dibuang, _ = olah_berkas("t.txt", isi, buang_teks_sama=True)
        self.assertEqual(len(item), 3)

    def test_wa_pesan_sama_pengirim_sama_hari_sama(self):
        isi = ("12/09/26 09.02 - Siti: rotinya gosong kak\n12/09/26 09.03 - Siti: rotinya gosong kak\n"
               "12/09/26 09.04 - Ani: rotinya gosong kak\n13/09/26 09.04 - Budi: enak sekali\n")
        item, _, dibuang, _ = olah_berkas("c.txt", isi)
        self.assertEqual(len(item), 3)
        self.assertEqual(dibuang.get("duplikat (baris identik)"), 1)


class UjiBerkasRusak(unittest.TestCase):
    """Permintaan 8: pesan GAGAL yang jelas (kode 2), bukan traceback; encoding UTF-16/BOM."""

    def rc(self, nama, isi, *arg):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, nama)
            if isi is not None:
                with open(p, "wb") as f:
                    f.write(isi)
            args = [p] + [a.replace("{d}", d) for a in arg]
            return jalankan_cli(args)

    def test_berkas_tidak_ada(self):
        rc, out, err = self.rc("hilang.txt", None)
        self.assertEqual(rc, 2)
        self.assertIn("GAGAL: berkas tidak ditemukan", err)
        self.assertNotIn("Traceback", err)

    def test_folder_dan_biner(self):
        with tempfile.TemporaryDirectory() as d:
            rc, _, err = jalankan_cli([d])
        self.assertEqual(rc, 2)
        self.assertIn("folder", err)
        rc, _, err = self.rc("b.csv", bytes(range(256)) * 20)
        self.assertEqual(rc, 2)
        self.assertIn("biner", err)
        rc, _, err = self.rc("b2.csv", bytes((i * 37 + 11) % 256 for i in range(3000)).replace(b"\x00", b"\x01"))
        self.assertEqual(rc, 2)

    def test_json_tema_rusak_dan_tidak_ada(self):
        with tempfile.TemporaryDirectory() as d:
            p = tulis(d, "t.txt", "rotinya enak sekali\n")
            j = tulis(d, "rusak.json", '{"tema": [ {"id": "x", ')
            rc, _, err = jalankan_cli([p, "--tema", j])
            self.assertEqual(rc, 2)
            self.assertIn("bukan JSON yang valid", err)
            rc, _, err = jalankan_cli([p, "--tema", os.path.join(d, "tidak.json")])
            self.assertEqual(rc, 2)
            j = tulis(d, "salah.json", '{"tema": [{"label": "tanpa id"}]}')
            rc, _, err = jalankan_cli([p, "--tema", j])
            self.assertEqual(rc, 2)
            self.assertIn("id", err)

    def test_kutip_tidak_seimbang(self):
        rc, _, err = self.rc("k.csv", b'Ulasan,Rating\n"rotinya gosong,1\nenak,5\n')
        self.assertEqual(rc, 2)
        self.assertIn("tanda kutip", err)

    def test_kosong(self):
        rc, _, err = self.rc("k.txt", b"   \n\n")
        self.assertEqual(rc, 2)
        self.assertIn("GAGAL", err)

    def test_utf16_bom_dan_tanpa_bom(self):
        teks = "kak rotinya keras bgt\nenak tp kemanisan\n"
        for data in (teks.encode("utf-16"), b"\xfe\xff" + teks.encode("utf-16-be"), teks.encode("utf-16-le"),
                     b"\xef\xbb\xbf" + teks.encode("utf-8")):
            item, _, _, _ = olah_berkas("u.txt", data)
            self.assertEqual([i["teks"] for i in item], ["kak rotinya keras bgt", "enak tp kemanisan"])

    def test_utf8_campur_cp1252_per_baris(self):
        data = "enak banget 😍 rotinya\n".encode("utf-8") + "roti basi “parah”\n".encode("cp1252")
        item, r, _, _ = olah_berkas("c.txt", data)
        self.assertIn("😍", item[0]["teks"])            # baris UTF-8 lain tidak rusak
        self.assertIn("“parah”", item[1]["teks"])
        self.assertTrue(any("Windows-1252" in p for p in r["peringatan"]))


class UjiTema(unittest.TestCase):
    """Permintaan 6-7: tema bawaan baru/netral usaha, tambah_kata, hapus_tema, contoh tema per usaha."""

    def setUp(self):
        self.tema, self.pos, self.neg = om.buat_tema(None)

    def tema_dari(self, teks, b=None, tema=None):
        t = tema or (self.tema, self.pos, self.neg)
        return om.analisis_item(teks, b, *t)[1]

    def test_tema_baru_dan_tidak_dobel(self):
        self.assertIn("waktu_tunggu", self.tema_dari("antrian lama, nunggu 30 menit"))
        self.assertIn("fasilitas", self.tema_dari("wifi sering putus, colokan kurang"))
        t = self.tema_dari("masih bau apek kak")
        self.assertIn("bau_aroma", t)
        self.assertNotIn("keamanan", t)
        self.assertNotIn("kemasan", self.tema_dari("setrikaannya rapi, wangi"))
        self.assertNotIn("varian_menu", self.tema_dari("paket sy blm dtg"))
        self.assertIn("stok_ketersediaan", self.tema_dari("kapan restock warna sage?"))
        self.assertEqual(self.tema_dari("warnanya pudar setelah dicuci", 2)["kualitas_produk"], {"keluhan"})
        self.assertEqual(self.tema_dari("ada rambut di nasi", 1)["keamanan"], {"keluhan"})

    def test_tambah_kata_tidak_mengganti_kata_bawaan(self):
        tema = om.buat_tema({"tambah_kata": {"layanan": ["dibales"]}})
        self.assertIn("layanan", self.tema_dari("chat ga dibales", tema=tema))
        self.assertIn("layanan", self.tema_dari("admin judes", tema=tema))

    def test_id_sama_mengganti_kata_bawaan(self):
        tema = om.buat_tema({"tema": [{"id": "layanan", "label": "Layanan", "kata": ["dibales"], "dampak": 3}]})
        self.assertNotIn("layanan", self.tema_dari("admin judes", tema=tema))

    def test_hapus_tema_dan_id_salah(self):
        tema = om.buat_tema({"hapus_tema": ["bau_aroma"]})
        self.assertNotIn("bau_aroma", self.tema_dari("bau apek", tema=tema))
        with self.assertRaises(om.Gagal):
            om.buat_tema({"tambah_kata": {"tidak_ada": ["x"]}})

    def test_peringatan_tema_dobel(self):
        konf = {"tema": [{"id": "bau_apek", "label": "Bau apek", "kata": ["apek"], "dampak": 4}]}
        _, r, _, _ = olah_berkas("c.txt", "bau apek kak\nmasih bau apek\napek lagi baunya\n", konfigurasi=konf)
        self.assertTrue(any("dobel" in p for p in r["peringatan"]))

    def test_semua_template_tema_valid(self):
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
        nama = sorted(f for f in os.listdir(folder) if f.startswith("tema-") and f.endswith(".json"))
        self.assertGreaterEqual(len(nama), 4)
        for f in nama:
            with open(os.path.join(folder, f), encoding="utf-8") as fh:
                om.buat_tema(json.load(fh))
        om.buat_tema(None)


class UjiTrenDanTampilan(unittest.TestCase):
    """Permintaan 9-10."""

    def test_tren_indikatif_dan_keluhan_sedikit(self):
        baris = ["Tanggal,Ulasan"]
        baris += ["2026-08-%02d,kurir telat parah nomor %d" % (i + 1, i) for i in range(3)]
        baris += ["2026-08-%02d,enak sekali nomor %d" % (i + 10, i) for i in range(3)]
        baris += ["2026-09-%02d,enak sekali nomor %d" % (i + 1, i + 20) for i in range(5)]
        baris += ["2026-09-%02d,rasanya hambar nomor %d" % (i + 10, i + 40) for i in range(1)]
        _, r, _, _ = olah_berkas("t.csv", "\n".join(baris))
        peng = [t for t in r["tema"] if t["id"] == "pengiriman"][0]
        self.assertEqual(peng["arah_tren"], "turun")
        self.assertTrue(peng["tren_indikatif"])
        rasa = [t for t in r["tema"] if t["id"] == "rasa"][0]
        self.assertEqual(rasa["arah_tren"], "keluhan terlalu sedikit")
        self.assertIsNone(rasa["selisih_persen_poin"])
        self.assertIn("indikatif: data kecil", om.cetak_teks(r, Opsi()))

    def test_perlu_dibaca_agent_tampil_semua(self):
        isi = "\n".join("halo apa kabar nomor %d" % i for i in range(25))
        _, r, _, _ = olah_berkas("t.txt", isi)
        teks = om.cetak_teks(r, Opsi())
        self.assertEqual(len(r["belum_terklasifikasi"]["contoh"]), 25)
        self.assertIn("+5 lainnya", teks)


class UjiPenyamaranLanjut(unittest.TestCase):
    """Permintaan 12-13."""

    def test_kasus_bocor_v100(self):
        kasus = {"makasih kak rina, enak": "rina", "Saya Budi mau komplain": "Budi", "transfer a.n. Siti Aminah ya": "Siti",
                 "telp 021 555 1234": "555", "kirim ke Perum Griya Asri Blok C2 No 5": "Griya", "plat B 1234 XYZ": "1234",
                 "Terima kasih mba Sari Lestari": "Lestari", "Pak RT Joko bilang enak": "Joko", "nama saya rina": "rina",
                 "alamat Gg. Kenanga 3 RT 04": "RT 04"}
        for teks, bocor in kasus.items():
            self.assertNotIn(bocor, om.samarkan(teks), teks)

    def test_tidak_berlebihan(self):
        for teks in ("kak mau komplain", "halo kak admin, pesanan telat", "Rp 25.000 untuk 2 porsi", "tanggal 12/09/2026 jam 08.15",
                     "Saya Mau pesan", "enak kak.", "size L 2 pcs"):
            self.assertEqual(om.samarkan(teks), teks)

    def test_nama_pengirim_bersapaan(self):
        t = om.samarkan("makasih kak paketnya udh sampe, bagus bgt kak", ["Kak Yanti"])
        self.assertEqual(t, "makasih kak paketnya udh sampe, bagus bgt kak")
        self.assertEqual(om.samarkan("Yanti bilang bagus", ["Kak Yanti"]), "[nama] bilang bagus")


if __name__ == "__main__":
    unittest.main(verbosity=1)
