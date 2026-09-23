#!/usr/bin/env python3
"""Uji regresi siapkan_broadcast.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "siapkan_broadcast.py")
PESAN = "Halo {sapaan} {nama}, promo roti hari ini.\nTidak ingin menerima info promo lagi? Balas STOP.\n---\n" \
        "Hai {sapaan} {nama}! Roti baru keluar oven.\nBalas BERHENTI untuk berhenti.\n"


def jalankan(kontak, pesan=PESAN, *arg):
    d = tempfile.mkdtemp()
    fk, fp, fo = (os.path.join(d, x) for x in ("k.csv", "p.txt", "o.csv"))
    with open(fk, "w", encoding="utf-8") as f:
        f.write(kontak)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(pesan)
    r = subprocess.run([sys.executable, SCRIPT, "--kontak", fk, "--pesan", fp, "--output", fo] + list(arg),
                       capture_output=True, text=True, encoding="utf-8")
    baris = []
    if r.returncode == 0:
        with open(fo, encoding="utf-8-sig") as f:
            baris = list(csv.DictReader(f))
    return r, baris


class Uji(unittest.TestCase):
    def test_b1_isi_kolom_berhenti_apa_pun_dianggap_berhenti(self):
        k = ("nama,nomor,persetujuan,berhenti\nSari,081200000001,ya,STOP\nTono,081200000002,ya,2026-09-01\n"
             "Ani,081200000003,ya,x\nBudi,081200000004,ya,tidak\nCici,081200000005,ya,\nDodi,081200000006,ya,-\n")
        r, b = jalankan(k)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(sorted(x["nama"] for x in b), ["Budi", "Cici", "Dodi"])

    def test_b2_duplikat_tidak_menimpa_berhenti_atau_tolak(self):
        k = ("nama,nomor,persetujuan,berhenti\nHadi,081200000010,ya,ya\nHadi Dup,+62 812-0000-0010,ya,\n"
             "Rini,081200000011,tidak,\nRini Dup,81200000011,ya,\nEka,081200000012,ya,\n")
        r, b = jalankan(k)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([x["nama"] for x in b], ["Eka"])
        self.assertIn("nomor ini minta berhenti/tidak setuju di baris lain", json.loads(r.stdout)["dilewati"])

    def test_jumat_1130_1300_dilewati(self):
        k = "nama,nomor,setuju\n" + "".join("O{0},0812{0:08d},ya\n".format(i) for i in range(10))
        # 2026-10-02 adalah hari Jumat
        r, b = jalankan(k, PESAN, "--mulai", "2026-10-02 11:26", "--jeda-pesan-detik", "60")
        self.assertEqual(r.returncode, 0, r.stderr)
        jam = [x["jadwal_kirim"][11:] for x in b]
        self.assertTrue(all(not ("11:30" <= j < "13:00") for j in jam), jam)
        self.assertIn("13:00", jam)
        r, b = jalankan(k, PESAN, "--mulai", "2026-10-02 11:26", "--kirim-saat-jumatan")
        self.assertIn("11:30", [x["jadwal_kirim"][11:] for x in b])

    def test_optout_longgar_ditolak(self):
        r, _ = jalankan("nama,nomor,setuju\nA,081200000001,ya\n", "Halo {nama}, promo non-stop sepanjang hari!\n")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("cara berhenti", r.stderr)

    def test_awalan_0062_dan_nama_hanya_sapaan(self):
        r, b = jalankan("nama,nomor,setuju\nBu,0062812000000099,ya\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(b[0]["nomor"], "62812000000099")
        self.assertTrue(b[0]["pesan"].startswith("Halo Bu,"), b[0]["pesan"])

    def test_tanpa_kolom_persetujuan_ditolak(self):
        r, _ = jalankan("nama,nomor\nA,081200000001\n")
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
