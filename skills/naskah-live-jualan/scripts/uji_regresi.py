#!/usr/bin/env python3
"""Uji regresi hitung_promo.py, susun_segmen.py & cek_fakta.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import unittest

DIR = os.path.dirname(os.path.abspath(__file__))


def jalan(script, *arg):
    r = subprocess.run([sys.executable, os.path.join(DIR, script)] + list(arg) + ["--json"],
                       capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout) if r.returncode == 0 else None)


class UjiPromo(unittest.TestCase):
    def test_format_angka(self):
        for teks, harap in (("1.500rb", 1500000), ("1,5jt", 1500000), ("1.5jt", 1500000), ("Rp 89.000", 89000),
                            ("89rb", 89000), ("89000", 89000)):
            r, h = jalan("hitung_promo.py", "--harga-normal", teks, "--harga-live", "1")
            self.assertEqual(h["harga_normal"], harap, teks)

    def test_bundling_sama_dengan_harga_live_diberi_peringatan(self):
        r, h = jalan("hitung_promo.py", "--harga-normal", "90000", "--harga-live", "75000", "--bundling", "2=150000")
        self.assertTrue(any("sama dengan" in p for p in h["peringatan"]))
        self.assertFalse(h["bundling"][0]["lebih_hemat_dari_harga_live"])

    def test_pembulatan_jujur(self):
        r, h = jalan("hitung_promo.py", "--harga-normal", "89000", "--diskon-persen", "12,5", "--bulatkan", "1000")
        self.assertEqual(h["harga_live"], 78000)          # 77.875 dibulatkan ke atas
        self.assertEqual(h["persen_hemat_boleh_diucapkan"], 12)  # 12,36% dibulatkan ke bawah
        self.assertNotIn("±", h["kalimat_live"])

    def test_input_rusak(self):
        for arg in (["--harga-normal", "abc", "--harga-live", "1"], ["--harga-normal", "89000", "--harga-live", "99000"],
                    ["--harga-normal", "89000", "--diskon-persen", "100"], ["--harga-normal", "89000", "--bundling", "1=5"]):
            r, _ = jalan("hitung_promo.py", *arg)
            self.assertEqual(r.returncode, 1, arg)


class UjiSegmen(unittest.TestCase):
    def cek(self, durasi, produk):
        r, h = jalan("susun_segmen.py", "--durasi", str(durasi), "--produk", produk)
        self.assertEqual(r.returncode, 0, r.stderr)
        seg = h["segmen"]
        self.assertEqual(seg[-1]["selesai_menit"], durasi)
        for a, b in zip(seg, seg[1:]):
            self.assertEqual(a["selesai_menit"], b["mulai_menit"])
        self.assertEqual({s["produk"] for s in seg if s["produk"] != "-"}, set(produk.split(",")))
        return seg

    def test_rekap_tiap_15_menit(self):
        for d in (45, 60, 90, 120):
            seg = self.cek(d, "A,B,C")
            titik = [s["mulai_menit"] for s in seg
                     if s["segmen"].startswith(("Pembukaan", "Rekap", "Tanya-jawab bebas", "Penutup"))]
            self.assertLessEqual(max(b - a for a, b in zip(titik, titik[1:])), 17, (d, titik))

    def test_semua_produk_kebagian_saat_waktu_mepet(self):
        self.cek(26, "A,B,C")
        self.cek(27, "A,B,C")

    def test_durasi_terlalu_pendek_ditolak(self):
        r, _ = jalan("susun_segmen.py", "--durasi", "20", "--produk", "A,B,C")
        self.assertEqual(r.returncode, 1)


FAKTA_MADU = ("Bikin naskah Shopee Live 30 menit buat jual madu hutan \"Madu Rimba\". Harganya emang Rp120.000 flat. "
              "Stok pake angka di layar aja. Toko Madu Rimba, host-nya aku sendiri, Rina. Kirim dari Pekanbaru, gak ada COD.")


def cek_fakta(teks, fakta, *ekstra):
    r = subprocess.run([sys.executable, os.path.join(DIR, "cek_fakta.py"), "--teks", teks, "--fakta", fakta, "--json"]
                       + list(ekstra), capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else None)


class UjiCekFakta(unittest.TestCase):
    def kategori_gagal(self, h):
        return {t["kategori"] for t in h["temuan"] if t["level"] == "GAGAL"}

    def test_kasus_madu_uji_ulang_2026_10_01_tertangkap(self):
        teks = ("**[19:00–19:03] Pembukaan**\n\"Malam ini Madu Rimba, madu hutan asli yang diambil langsung dari "
                "Pekanbaru.\"\n\"Bisa jadi pendamping harian buat jaga stamina dan daya tahan tubuh.\"\n"
                "\"Isinya 250ml Kak.\"")
        r, h = cek_fakta(teks, FAKTA_MADU)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.kategori_gagal(h), {"jam", "asal", "klaim", "ukuran"})
        frasa = " ".join(t["frasa"] for t in h["temuan"])
        self.assertIn("diambil langsung dari Pekanbaru", frasa)
        self.assertIn("jaga stamina", frasa)

    def test_naskah_jujur_lulus(self):
        teks = ("**[menit 0–3] Pembukaan**\n\"Halo Kak, selamat datang di live Madu Rimba, saya Rina. Madu hutan ini "
                "dikirim dari Pekanbaru ya Kak.\" [tunjukkan tekstur]\n\"Teksturnya [isi: kental/cair], isi per botol "
                "[isi: ukuran 250ml/350gr?].\"\n| \"Bisa nyembuhin diabetes?\" | \"Kami tidak bisa menjanjikan hasil "
                "medis ya Kak, bukan obat.\" |\n- Asumsi: jam mulai belum disebut — isi sendiri.")
        r, h = cek_fakta(teks, FAKTA_MADU)
        self.assertEqual(r.returncode, 0, h)
        self.assertEqual(h["hasil"], "LULUS")

    def test_jam_boleh_bila_disebut_pengguna(self):
        r, h = cek_fakta("[20:00–20:03] Pembukaan", "Live mulai jam 8 malem, toko Sambal Bu Rum dari Surabaya.")
        self.assertEqual(r.returncode, 0, h)
        r, h = cek_fakta("- Asumsi: mulai 19:00 (belum disebut pengguna).", FAKTA_MADU)
        self.assertEqual(r.returncode, 0, h)
        self.assertEqual([t["level"] for t in h["temuan"]], ["CEK"])

    def test_khas_kota_toko_ditolak_tetapi_kirim_dari_boleh(self):
        fakta = "toko Sambal Bu Rum dari Surabaya. Kirim tiap hari, bisa COD."
        r, h = cek_fakta("\"Sambal bawang khas Surabaya, dikirim tiap hari dari Surabaya.\"", fakta)
        self.assertEqual([t["frasa"] for t in h["temuan"]], ["khas Surabaya"])
        r, h = cek_fakta("\"Madu ini dipanen dari hutan Riau.\"", "Madu hutan dipanen dari hutan Riau.")
        self.assertEqual(r.returncode, 0, h)

    def test_reputasi_dari_pengguna_tanpa_bukti_jadi_cek(self):
        fakta = "Tulis juga kalau produk kita paling laris se-Solo."
        r, h = cek_fakta("Produk terlaris di Solo.", fakta)
        self.assertEqual((r.returncode, h["temuan"][0]["level"]), (0, "CEK"))
        r, h = cek_fakta("Produk terlaris di Solo [isi: bukti data penjualan].", fakta)
        self.assertEqual(h["temuan"], [])
        r, h = cek_fakta("Sudah dikenal pelanggan di Solo.", fakta)
        self.assertEqual(r.returncode, 2)

    def test_pertanyaan_negasi_dan_nomor_etalase_diabaikan(self):
        teks = ("| \"Ini madu asli apa campuran?\" | \"Detail ada di deskripsi produk Kak.\" |\n"
                "\"Klik keranjang, pilih nomor 1, lalu checkout.\"\n- Tidak ada klaim menyembuhkan di naskah ini.")
        r, h = cek_fakta(teks, FAKTA_MADU)
        self.assertEqual(r.returncode, 0, h)

    def test_menyembuhkan_selalu_gagal_walau_diminta(self):
        r, h = cek_fakta("\"Madu ini menyembuhkan asam lambung.\"", "bilang madunya bisa menyembuhkan asam lambung")
        self.assertEqual(r.returncode, 2)

    def test_input_salah(self):
        for arg in (["--teks", "x"], ["--teks", "x", "--fakta", "  "], ["--fakta", "x"],
                    ["--teks", "x", "--fakta", "y", "--abaikan", "warna"]):
            r = subprocess.run([sys.executable, os.path.join(DIR, "cek_fakta.py")] + arg, capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, arg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
