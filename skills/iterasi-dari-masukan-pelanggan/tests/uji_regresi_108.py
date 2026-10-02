#!/usr/bin/env python3
"""
uji_regresi_108.py - uji regresi v1.0.8 (temuan uji OpenClaw sebelum/sesudah, toko kue "Kue Nara", 2026-10-02).

1. Kosakata tekstur kue/roti: "bantat", "tengahnya basah" = keluhan Rasa/tekstur ("tidak bantat" = pujian).
2. "bintik hijau"/"bintik putih berbulu"/"jamuran" = Keamanan (jamur); "roti sobek" = nama produk, bukan barang robek.
3. Keterlambatan tanpa kata "telat": "nyampe jam 4 padahal janjinya jam 10", "acara udah bubar", "baru nyampe jumat padahal pesan
   senin", "lama banget pesanan saya", "3 hari belum datang" = keluhan Pengiriman; "baru sampai langsung dicoba, enak" bukan keluhan.
4. Respons staf: pesan/keluhan WA yang tidak dibalas staf (--staf) dihitung; kolom balasan penjual di CSV dihitung.
5. Sentimen per kanal dicetak script (agent tidak menghitung sendiri).
6. --koreksi: koreksi agent tercatat & dihitung ulang script.

Kalimat contoh 1-3 diambil dari berkas uji (examples/00-openclaw-sebelum-sesudah.md); data fiktif.
Jalankan (dari folder skill): python3 tests/uji_regresi_108.py
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
import olah_masukan as om  # noqa: E402


def analisis(teks, bintang=None):
    tema, pos, neg = om.buat_tema(None)
    a = om.samarkan(teks)
    sent, pt = om.analisis_item(a, bintang, tema, pos, neg)
    return sent, {k for k, v in pt.items() if "keluhan" in v}, {k for k, v in pt.items() if "pujian" in v}


WA = """[01/09/2026 08.12.30] Pelanggan Satu: Kak, brownies kemarin enak banget
[01/09/2026 08.20.00] Admin Toko: Terima kasih kak 🙏
[03/09/2026 10.06.40] Pelanggan Dua: Oiya bolu pandan minggu lalu agak bantat, tengahnya basah
[05/09/2026 19.30.00] Pelanggan Tiga: Ini roti sobeknya kok ada bintik hijau kak? Anak saya sudah makan setengah 😡
[05/09/2026 19.31.00] Pelanggan Tiga: <Media tidak disertakan>
[05/09/2026 19.45.00] Admin Toko: Mohon maaf bu, kami cek segera
[08/09/2026 09.00.00] Pelanggan Empat: Paket nyampe jam 4 sore padahal janjinya jam 10 pagi. acara arisan udah bubar
[12/09/2026 16.40.00] Pelanggan Lima: mantap, chat dari pagi baru dibalas sore 👍
[22/09/2026 10.00.00] Pelanggan Enam: Kotak kuenya penyok, krimnya nempel ke tutup
[25/09/2026 10.00.00] Admin Toko: Mohon maaf kak, kami ganti ya
[26/09/2026 15.20.00] Pelanggan Tujuh: Pengiriman telat lagi kak, 3 jam. Tolong dibenahi
"""
CSV_ULASAN = """Nama Pembeli,Tanggal,Rating,Ulasan,Balasan Penjual
A,2026-09-02,5,"Brownies fudgy, enak banget, packing rapi",Terima kasih kak
B,2026-09-06,1,"Roti berjamur padahal tanggal kadaluarsa masih lama. Kecewa",
C,2026-09-09,3,"Lumayan, bolu agak bantat",
D,2026-09-13,2,"Pengiriman lama banget, 4 hari baru sampai, roti sudah keras",Mohon maaf kak
E,2026-09-14,5,"Admin ramah dan fast respon",
"""


class Opsi:
    staf_list = []
    kolom_teks = kolom_bintang = kolom_tanggal = skala = None
    buang_teks_sama = False
    contoh = 3
    min_bulan = 5
    urutan_tanggal = None
    batas_balas_jam = 24
    koreksi = None


class UjiKosakata108(unittest.TestCase):
    def test_bantat_dan_tengah_basah(self):
        for t, b in [("Oiya bolu pandan minggu lalu agak bantat, tengahnya basah", None), ("Lumayan, bolu agak bantat", 3),
                     ("brownies tengahnya masih mentah", None)]:
            self.assertIn("rasa", analisis(t, b)[1], t)
        self.assertNotIn("rasa", analisis("kue keringnya renyah, tidak bantat")[1])

    def test_bintik_hijau_jamur_keamanan(self):
        for t in ["Ini roti sobeknya kok ada bintik hijau kak? baru beli kemarin. Anak saya sudah makan setengah 😡",
                  "rotinya ada bintik putih berbulu", "roti tawarnya jamuran", "Kak ini roti tawarnya baru 2 hari udah berjamur lagi"]:
            kel = analisis(t)[1]
            self.assertIn("keamanan", kel, t)
        # "roti sobek" = nama produk: tidak boleh jadi keluhan kualitas "robek"
        self.assertNotIn("kualitas_produk", analisis("Ini roti sobeknya kok ada bintik hijau kak?")[1])
        self.assertEqual(analisis("roti sobeknya enak, lembut")[1], set())

    def test_telat_tanpa_kata_telat(self):
        for t in ["Paket nyampe jam 4 sore padahal janjinya jam 10 pagi. acara arisan udah bubar",
                  "kuenya datang pas acara sudah bubar", "Pesanan saya baru nyampe hari jumat, padahal pesan senin",
                  "pesan senin baru sampai jumat", "kok lama banget kak pesanan saya", "paket saya kok lama ya",
                  "sudah 3 hari belum datang kak kuenya", "3 hari belum datang pesanan saya",
                  "Pengiriman lama banget, 4 hari baru sampai, roti sudah keras"]:
            self.assertIn("pengiriman", analisis(t)[1], t)

    def test_bukan_telat(self):
        for t in ["baru sampai langsung dicoba, enak banget", "Kue datang tepat waktu, enak", "MC stay sampai acara selesai, mantap",
                  "kuenya tahan lama, enak"]:
            self.assertNotIn("pengiriman", analisis(t)[1], t)

    def test_kata_bernya_bukan_nama(self):
        self.assertIn("kuenya", om.samarkan("sudah 3 hari belum datang kak kuenya"))
        self.assertIn("[nama]", om.samarkan("makasih kak rina"))


def _jalankan(tmp, staf=("Admin Toko",), koreksi=None):
    wa, cs = os.path.join(tmp, "chat.txt"), os.path.join(tmp, "ulasan.csv")
    for path, isi in ((wa, WA), (cs, CSV_ULASAN)):
        with open(path, "w", encoding="utf-8") as f:
            f.write(isi)
    o = Opsi()
    o.staf_list = list(staf)
    o.koreksi = koreksi
    item, tema, dibuang, meta = om.olah(["%s=WhatsApp" % wa, "%s=Shopee" % cs], o)
    return om.ringkas(item, tema, dibuang, o, meta), item


class UjiRespons108(unittest.TestCase):
    def test_wa_tidak_dibalas(self):
        with tempfile.TemporaryDirectory() as tmp:
            r, item = _jalankan(tmp)
        wa = r["respons_staf"]["WhatsApp"]
        # dibalas <= 24 jam: pesan 1 & pesan bintik hijau; kotak penyok dibalas 3 hari kemudian (lambat)
        self.assertEqual((wa["masukan"], wa["dibalas"]), (7, 2))
        self.assertEqual(wa["keluhan_dibalas_lambat"], 1)
        self.assertEqual(wa["keluhan_tanpa_balasan"], 4)   # bantat, telat janji, sindiran, telat 3 jam
        self.assertTrue(any("bantat" in c for c in wa["contoh_tanpa_balasan"]))
        sh = r["respons_staf"]["Shopee"]
        self.assertEqual((sh["masukan"], sh["dibalas"], sh["keluhan"], sh["keluhan_tanpa_balasan"]), (5, 2, 3, 2))

    def test_tanpa_staf_tidak_dihitung(self):
        with tempfile.TemporaryDirectory() as tmp:
            r, _ = _jalankan(tmp, staf=())
        self.assertNotIn("WhatsApp", r["respons_staf"])
        self.assertIn("--staf", om.cetak_teks(r, Opsi()))

    def test_staf_salah_nama_peringatan(self):
        with tempfile.TemporaryDirectory() as tmp:
            r, _ = _jalankan(tmp, staf=("Bukan Siapa",))
        self.assertNotIn("WhatsApp", r["respons_staf"])
        self.assertTrue(any("tidak ada pesan dari staf" in p for p in r["peringatan"]))

    def test_sentimen_per_kanal(self):
        with tempfile.TemporaryDirectory() as tmp:
            r, _ = _jalankan(tmp)
        self.assertEqual(r["sentimen_per_kanal"]["Shopee"], {"positif": 2, "netral": 1, "negatif": 2})
        total = {k: sum(v[k] for v in r["sentimen_per_kanal"].values()) for k in ("positif", "netral", "negatif")}
        self.assertEqual(total, r["sentimen"])
        self.assertIn("Shopee: positif 2, netral 1, negatif 2", om.cetak_teks(r, Opsi()))


class UjiKoreksi108(unittest.TestCase):
    def test_koreksi_diterapkan_dan_dihitung_ulang(self):
        with tempfile.TemporaryDirectory() as tmp:
            r0, _ = _jalankan(tmp)
            k = os.path.join(tmp, "koreksi.csv")
            with open(k, "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["cuplikan", "tema", "jenis", "sentimen", "catatan"])
                w.writerow(["baru dibalas sore", "layanan", "keluhan", "negatif", "sindiran"])
                w.writerow(["tidak ada di data", "layanan", "keluhan", "", ""])
                w.writerow(["bolu agak bantat", "temaxyz", "keluhan", "", ""])
            r1, item = _jalankan(tmp, koreksi=k)
        lay0 = next((d["keluhan"] for d in r0["tema"] if d["id"] == "layanan"), 0)
        lay1 = next(d["keluhan"] for d in r1["tema"] if d["id"] == "layanan")
        self.assertEqual(lay1, lay0 + 1)
        self.assertEqual(r1["sentimen"]["negatif"], r0["sentimen"]["negatif"] + 1)
        self.assertEqual(len(r1["koreksi"]), 1)
        self.assertTrue(any("tidak ditemukan" in p for p in r1["peringatan"]))
        self.assertTrue(any("tema tidak dikenal" in p for p in r1["peringatan"]))
        self.assertFalse(any("baru dibalas sore" in d["teks"] for d in r1["perlu_dibaca"]["daftar"]))

    def test_koreksi_rusak_gagal(self):
        with tempfile.TemporaryDirectory() as tmp:
            k = os.path.join(tmp, "koreksi.csv")
            with open(k, "w", encoding="utf-8") as f:
                f.write("teks,tema\nabc,layanan\n")
            with self.assertRaises(om.Gagal):
                _jalankan(tmp, koreksi=k)

    def test_cli_koreksi_dan_simpan(self):
        with tempfile.TemporaryDirectory() as tmp:
            wa, an = os.path.join(tmp, "chat.txt"), os.path.join(tmp, "an.csv")
            with open(wa, "w", encoding="utf-8") as f:
                f.write(WA)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                kode = om.main([wa + "=WhatsApp", "--staf", "Admin Toko", "--koreksi", str(SKILL_DIR / "templates" / "koreksi-contoh.csv"),
                                "--simpan-anonim", an])
            self.assertEqual(kode, 0)
            teks = out.getvalue()
            self.assertIn("Koreksi agent diterapkan", teks)
            self.assertIn("keluhan TANPA balasan", teks)
            with open(an, encoding="utf-8") as f:
                baris = list(csv.DictReader(f))
            self.assertIn("dibalas", baris[0])
            self.assertTrue(any(b["koreksi"] for b in baris))


if __name__ == "__main__":
    unittest.main(verbosity=1)
