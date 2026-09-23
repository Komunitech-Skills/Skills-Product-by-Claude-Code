#!/usr/bin/env python3
"""
uji_regresi.py — Uji regresi untuk scripts/periksa_draf.py (agen-cs-toko).

Berisi seluruh kasus dari examples/HASIL-UJI.md: 17 kasus regresi awal +
kasus baru dari "Uji ulang v1.0.1" (harga tanpa Rp dengan nama produk di
tengah, positif palsu persen/satuan/tahun/kode pos, regresi keamanan OTP,
konteks NIK vs nomor pesanan, basis pengetahuan non-UTF-8, dst.).

Jalankan:
    python3 tests/uji_regresi.py
    python3 -m unittest tests.uji_regresi -v   (dari folder skill)

Semua kasus harus LULUS (exit 0 bila dijalankan langsung).
"""

import pathlib
import sys
import unittest

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import periksa_draf as pd  # noqa: E402

KB_DASAR = """
| Nama | Harga |
|---|---|
| Pashmina Ceruti | Rp 89.000 |
| Bergo | Rp 65.000 |
| Voal | Rp 125.000 |
| Paket 3 | Rp 240.000 |
Gratis ongkir min. Rp 300.000
"""

# Basis pengetahuan yang sengaja tanpa "Rp" untuk uji poin 6.
KB_TANPA_RP = """
Pashmina 89.000
Bergo 65.000
"""


def harga_draf(teks, kb=KB_DASAR):
    """Set nominal yang dianggap "tidak ada di basis pengetahuan"."""
    nominal_kb = pd.ekstrak_nominal(kb)
    nominal_draf = pd.ekstrak_nominal(teks)
    return sorted(nominal_draf - nominal_kb)


class UjiEkstraksiHarga(unittest.TestCase):
    # --- 17 kasus regresi lama -------------------------------------------------
    def test_01_normal_semua_cocok(self):
        self.assertEqual(harga_draf("Pashmina Rp 89.000 ya Kak, bergo Rp 65.000."), [])

    def test_02_karang_rp_79000(self):
        self.assertEqual(harga_draf("Ada promo Rp 79.000 khusus hari ini."), [79000])

    def test_03_karang_harganya_79000_tanpa_rp(self):
        self.assertEqual(harga_draf("Voal harganya 79.000 aja Kak."), [79000])

    def test_04_karang_1_5_juta(self):
        self.assertEqual(harga_draf("Paket lengkap jadi 1,5 juta ya Kak."), [1_500_000])

    def test_05_pashmina_89rb_benar(self):
        self.assertEqual(harga_draf("Pashmina Rp 89rb Kak, stok ready."), [])

    def test_06_karang_79rb(self):
        self.assertEqual(harga_draf("Voal cuma 79rb aja deh Kak."), [79000])

    def test_07_rp_1500000_koma_50(self):
        self.assertEqual(harga_draf("Total belanja Rp 1.500.000,50 ya."), [1_500_000])

    def test_08_total_turunan_178rb_vs_89rb_di_kb(self):
        self.assertEqual(
            harga_draf("Total turunan Rp 178.000 (2 x Rp 89.000)."), [178000]
        )

    def test_09_stok_tinggal_2_tidak_diperiksa(self):
        self.assertEqual(harga_draf("Stok tinggal 2 aja nih Kak."), [])

    def test_10_nik_otp_bocor(self):
        temuan = pd.cek_data_sensitif(
            "Boleh kirim NIK 3201010101010001 dan kode OTP yang masuk tadi."
        )
        jenis = [t["jenis"] for t in temuan]
        self.assertIn("NIK/nomor identitas 16 digit", jenis)
        self.assertIn("Kata kunci OTP", jenis)
        self.assertEqual(jenis.count("NIK/nomor identitas 16 digit"), 1)
        self.assertNotIn("Nomor kartu (mirip kartu debit/kredit)", jenis)

    def test_11_kartu_cvv(self):
        temuan = pd.cek_data_sensitif("Nomor kartu 4111 1111 1111 1111 dan cvv 123 ya.")
        jenis = [t["jenis"] for t in temuan]
        self.assertIn("Nomor kartu (mirip kartu debit/kredit)", jenis)
        self.assertIn("CVV/CVC kartu", jenis)

    def test_12_peringatan_jangan_otp_tanpa_kode(self):
        temuan = pd.cek_data_sensitif(
            "Ingat ya Kak, jangan kirim kode OTP ke siapa pun termasuk ke kami."
        )
        self.assertEqual(temuan, [])

    def test_12b_peringatan_tidak_pernah_otp_tanpa_kode(self):
        temuan = pd.cek_data_sensitif("Kami tidak pernah memerlukan kode OTP Kakak.")
        self.assertEqual(temuan, [])

    def test_13_no_hp_bersih(self):
        self.assertEqual(pd.cek_data_sensitif("Nomor kami 0812-0000-1234 ya Kak."), [])

    def test_14_nomor_pesanan_16_digit_bersih(self):
        temuan = pd.cek_data_sensitif("Nomor pesanan Kakak adalah 3201010101010001 ya.")
        self.assertEqual(temuan, [])

    def test_15_kirim_pin_lokasi_bersih(self):
        self.assertEqual(pd.cek_data_sensitif("Boleh kirim pin lokasi rumah Kakak?"), [])

    def test_16_basis_kosong_rp79000_ditandai(self):
        self.assertEqual(harga_draf("Boleh Kak, Rp 79.000 aja.", kb=""), [79000])

    def test_17_file_tidak_ada_exit_2(self):
        import subprocess

        hasil = subprocess.run(
            [sys.executable, str(SKILL_DIR / "scripts" / "periksa_draf.py"),
             "--pengetahuan", "/tidak/ada/file.md", "--draf", "-"],
            input="halo", capture_output=True, text=True,
        )
        self.assertEqual(hasil.returncode, 2)

    # --- Kasus baru "Uji ulang v1.0.1" -----------------------------------------
    def test_18_harga_produk_di_tengah_kata_kunci_dan_angka(self):
        self.assertEqual(harga_draf("Harga Pashmina Ceruti 79.000 ya Kak"), [79000])

    def test_19_harga_produk_tanpa_kata_kunci_depan(self):
        self.assertEqual(harga_draf("Pashmina Ceruti 79.000 aja Kak"), [79000])

    def test_20_idr_dikenali(self):
        self.assertEqual(harga_draf("IDR 79.000 ya Kak"), [79000])

    def test_21_cuma_55rb_per_pcs(self):
        self.assertEqual(harga_draf("Voal cuma 55rb/pcs ya."), [55000])

    def test_22_99k(self):
        self.assertEqual(harga_draf("Bergo 99k aja."), [99000])

    def test_23_rp_titik_dan_minus(self):
        self.assertEqual(harga_draf("Rp. 79.000,- ya Kak."), [79000])

    def test_24_harganya_jadi_199000_dengan_titik(self):
        self.assertEqual(harga_draf("Voal harganya jadi 199.000 ya."), [199000])

    def test_25_diskon_20_persen_bersih(self):
        self.assertEqual(harga_draf("Diskon 20% khusus hari ini ya Kak."), [])

    def test_26_jadi_3_pcs_bersih(self):
        self.assertEqual(harga_draf("Kalau jadi 3 pcs ya Kak, sekalian."), [])

    def test_27_promo_tahun_2026_bersih(self):
        self.assertEqual(harga_draf("Promo spesial tahun 2026 buat Kakak."), [])

    def test_28_promo_11_11_bersih(self):
        self.assertEqual(harga_draf("Promo 11.11 lagi jalan ya Kak."), [])

    def test_29_kode_pos_bukan_harga(self):
        self.assertEqual(harga_draf("Kode pos kami 17111 ya Kak."), [])

    def test_30_ongkir_1_2_hari_bersih(self):
        self.assertEqual(harga_draf("Ongkir estimasi 1-2 hari ya Kak."), [])

    def test_31_berat_dan_dimensi_bersih(self):
        self.assertEqual(harga_draf("Berat barang 1 kg, ukuran 110x110 cm."), [])

    def test_32_kode_booking_pesanan_bersih_harga(self):
        self.assertEqual(harga_draf("Kode booking pesanan 123456 ya Kak."), [])

    def test_33_basis_pengetahuan_tanpa_rp_dikenali(self):
        # KB tanpa "Rp": "Pashmina 89.000". Draf pakai "Rp 89.000" (nilai sama) -> bersih.
        self.assertEqual(harga_draf("Pashmina Rp 89.000 ya Kak.", kb=KB_TANPA_RP), [])

    def test_34_draf_stdin_masih_jalan(self):
        import subprocess

        proses = subprocess.run(
            [sys.executable, str(SKILL_DIR / "scripts" / "periksa_draf.py"),
             "--pengetahuan", "-", "--draf", "-"],
            input="TIDAK_DIPAKAI", capture_output=True, text=True,
        )
        # --pengetahuan - dan --draf - dua-duanya stdin: hanya menegaskan
        # tidak error/traceback (exit 0 atau 1, bukan crash python).
        self.assertIn(proses.returncode, (0, 1))


class UjiDataSensitifBaru(unittest.TestCase):
    def test_35_regresi_jangan_kode_otp_dengan_angka_HARUS_ditandai(self):
        temuan = pd.cek_data_sensitif(
            "Jangan kasih tau siapa2 ya Kak, kode OTP 482913."
        )
        self.assertTrue(temuan, "Harus ditandai: kalimat peringatan TAPI memuat kode 6 digit")

    def test_36_untuk_order_ini_nik_harus_ditandai(self):
        temuan = pd.cek_data_sensitif(
            "Untuk order ini NIK 3201010101010001 sudah kami simpan."
        )
        jenis = [t["jenis"] for t in temuan]
        self.assertIn("NIK/nomor identitas 16 digit", jenis)

    def test_37_nik_berspasi_tetap_ditandai(self):
        temuan = pd.cek_data_sensitif("NIK: 3201 0101 0101 0001 ya Kak.")
        self.assertTrue(temuan)

    def test_38_pin_atm_ditandai(self):
        temuan = pd.cek_data_sensitif("Boleh info PIN ATM 123456?")
        jenis = [t["jenis"] for t in temuan]
        self.assertIn("Kata kunci PIN", jenis)

    def test_39_password_ditandai(self):
        temuan = pd.cek_data_sensitif("Password akun Kakak apa ya?")
        jenis = [t["jenis"] for t in temuan]
        self.assertIn("Kata kunci password/kata sandi", jenis)

    def test_40_kodenya_482913_ditandai_tanpa_kata_otp(self):
        temuan = pd.cek_data_sensitif("Baik Kak, kodenya 482913 ya.")
        self.assertTrue(temuan)

    def test_41_kode_pos_bukan_data_sensitif(self):
        self.assertEqual(pd.cek_data_sensitif("Kode pos kami 17111 ya Kak."), [])

    def test_42_kode_booking_pesanan_bukan_data_sensitif(self):
        self.assertEqual(pd.cek_data_sensitif("Kode booking pesanan 123456 ya Kak."), [])


class UjiBacaTeks(unittest.TestCase):
    def test_43_basis_pengetahuan_cp1252_tidak_traceback(self):
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            # "café" dalam Windows-1252/Latin-1 (byte 0xE9 = 'é'), bukan UTF-8 valid berdiri sendiri.
            f.write("Kopi caf\xe9 Rp 25.000".encode("cp1252"))
            path = f.name
        try:
            teks = pd.baca_teks(path)
            self.assertIn("25.000", teks)
        finally:
            import os

            os.unlink(path)

    def test_44_file_tidak_ada_exit_2_bukan_traceback(self):
        with self.assertRaises(SystemExit) as ctx:
            pd.baca_teks("/path/sangat/tidak/ada/xyz123.md")
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
