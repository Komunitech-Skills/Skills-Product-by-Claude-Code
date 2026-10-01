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

    def test_b3_daftar_berhenti_bercatatan(self):
        k = ("nama,nomor,setuju\nPutri,081200000120,ya\nGalih,081200000139,ya\nHana,081200000140,ya\n"
             "Ika,081200000141,ya\nJoko,081200000142,ya\nLia,081200000143,ya\nMira,081200000144,ya\n")
        d = tempfile.mkdtemp()
        fs = os.path.join(d, "stop.txt")
        with open(fs, "w", encoding="utf-8") as f:
            f.write("Nama;No HP;Tanggal\n0812-0000-0120 tgl 12/09\nGalih 0812 0000 0139 (minta stop 2026-09-01)\n"
                    "0812-0000-0140\t Hana\n+62 812-0000-0141 - Ika\n0812 0000 0142 0812 0000 0143\n")
        r, b = jalankan(k, PESAN, "--daftar-berhenti", fs)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([x["nama"] for x in b], ["Mira"])
        h = json.loads(r.stdout)
        self.assertEqual(h["daftar_berhenti_terbaca"], 6)
        self.assertEqual(h["status"], "SIAP")

    def test_b3_baris_tak_terbaca_diperingatkan(self):
        d = tempfile.mkdtemp()
        fs = os.path.join(d, "stop.txt")
        with open(fs, "w", encoding="utf-8") as f:
            f.write("0812-000 (nomor terpotong)\n081200000150\n")
        r, _ = jalankan("nama,nomor,setuju\nA,081200000151,ya\n", PESAN, "--daftar-berhenti", fs)
        h = json.loads(r.stdout)
        self.assertEqual(h["status"], "PERIKSA DULU")
        self.assertEqual(h["daftar_berhenti_tidak_terbaca"][0]["baris"], 1)
        self.assertTrue(any("JANGAN kirim" in p for p in h["peringatan"]))

    def test_s1_optout_harus_instruksi(self):
        k = "nama,nomor,setuju\nA,081200000001,ya\n"
        for teks in ("Halo {nama}, siapa yang tidak mau dapat diskon 50%?",
                     "Halo {nama}. Kalau tidak ingin menerima kabar diskon, sayang banget lho",
                     "Halo {nama}, lauk siap saji untuk berhenti pusing mikir lauk",
                     "Halo {nama}, STOP! Jangan lewatkan promo"):
            r, _ = jalankan(k, teks)
            self.assertNotEqual(r.returncode, 0, teks)
        r, _ = jalankan(k, "Halo {nama}. Ketik \"stop\" kalau tidak mau dapat info lagi.")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_s2_gelar_dilewati(self):
        nama = ["IBU HJ. AMINAH", "dr. Andi", "H. Rahmat", "Pak H. Ahmad", "Hj. Siti Aminah", "Prof. Dr. Ir. Joko",
                "Sdr. Tono", "Andi, S.E."]
        harap = ["Bu Aminah", "Kak Andi", "Pak Rahmat", "Pak Ahmad", "Bu Siti", "Kak Joko", "Kak Tono", "Kak Andi"]
        k = "nama,nomor,setuju\n" + "".join('"{}",0812000002{:02d},ya\n'.format(n, i) for i, n in enumerate(nama))
        r, b = jalankan(k, "Halo {sapaan} {nama}!\nBalas STOP untuk berhenti.\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([x["pesan"].split("!")[0][5:] for x in b], harap)

    def test_nilai_tidak_baku_dilaporkan(self):
        k = "nama,nomor,persetujuan,berhenti\nA,081200000301,ya (lisan),\nB,081200000302,ya,masih aktif\n" \
            "C,081200000303,ya,\n"
        r, b = jalankan(k)
        alasan = " ".join(json.loads(r.stdout)["dilewati"])
        self.assertIn("ya (lisan)", alasan)
        self.assertIn("masih aktif", alasan)
        self.assertEqual([x["nama"] for x in b], ["C"])

    def test_b3b_angka_catatan_tidak_tergabung(self):
        baris_stop = ["0812 0000 0221 25 September", "0812-0000-0203 (2)", "0812-0000-0202 - 3x minta",
                      "0812 0000 0201 12 Sept 2026", "0812 0000 0224 - 17 Agustus", "5. 0812-0000-0215",
                      "1) 0812 0000 0216", "0812 0000 0204 jam 10.30", "0812-0000-0223 x2"]
        akhir = ["0221", "0203", "0202", "0201", "0224", "0215", "0216", "0204", "0223"]
        k = "nama,nomor,setuju\n" + "".join("S{0},08120000{0},ya\n".format(x) for x in akhir) + \
            "Aman,081200000999,ya\n"
        d = tempfile.mkdtemp()
        fs = os.path.join(d, "stop.txt")
        with open(fs, "w", encoding="utf-8") as f:
            f.write("\n".join(baris_stop) + "\n")
        r, b = jalankan(k, PESAN, "--daftar-berhenti", fs)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([x["nama"] for x in b], ["Aman"])
        h = json.loads(r.stdout)
        self.assertEqual(h["daftar_berhenti_terbaca"], 9)
        self.assertEqual(h["status"], "SIAP")

    def test_b3b_jaring_pengaman_nomor_stop_tak_cocok(self):
        d = tempfile.mkdtemp()
        fs = os.path.join(d, "stop.txt")
        with open(fs, "w", encoding="utf-8") as f:
            f.write("0812-0000-0777\n")
        r, b = jalankan("nama,nomor,setuju\nA,081200000001,ya\n", PESAN, "--daftar-berhenti", fs)
        h = json.loads(r.stdout)
        self.assertEqual(h["status"], "PERIKSA DULU")
        self.assertEqual(h["daftar_berhenti_tidak_cocok_kontak"][0]["baris"], [1])

    def test_optout_v102(self):
        k = "nama,nomor,setuju\nA,081200000001,ya\n"
        for teks in ("Halo {nama}, jangan balas STOP ya", "Halo {nama}, jangan sampai kirim berhenti",
                     "Halo {nama}. Ketik stop-motion untuk video"):
            self.assertNotEqual(jalankan(k, teks)[0].returncode, 0, teks)
        for teks in ("Halo {nama}. Balas dengan kata STOP untuk berhenti.", "Halo {nama}. Berhenti? balas: STOP"):
            self.assertEqual(jalankan(k, teks)[0].returncode, 0, teks)

    def test_gelar_v102(self):
        nama = ["Hj.Nurul", "Dr.Rina", "H.M. Yusuf", "Ny. Susi", "Tn. Budi", "Muh. Rizki"]
        harap = ["Bu Nurul", "Kak Rina", "Pak Yusuf", "Bu Susi", "Pak Budi", "Kak Rizki"]
        k = "nama,nomor,setuju\n" + "".join('"{}",0812000004{:02d},ya\n'.format(n, i) for i, n in enumerate(nama))
        r, b = jalankan(k, "Halo {sapaan} {nama}!\nBalas STOP untuk berhenti.\n")
        self.assertEqual([x["pesan"].split("!")[0][5:] for x in b], harap)
        k = 'nama,nomor,setuju\n"Dra. Hj. Sri Mulyani, M.Pd.",081200000501,ya\n"Drs. H. Tono, M.Si.",081200000502,ya\n'
        r, b = jalankan(k, "Halo {sapaan} {nama}!\nBalas STOP untuk berhenti.\n", "--nama-lengkap")
        self.assertEqual([x["pesan"].split("!")[0][5:] for x in b], ["Bu Sri Mulyani", "Pak Tono"])

    def test_v103_baris_tanpa_nomor_dan_huruf_o(self):
        d = tempfile.mkdtemp()
        fs = os.path.join(d, "stop.txt")
        with open(fs, "w", encoding="utf-8") as f:
            f.write("Daftar berhenti\n0812-OOOO-0332\nBu Tuti minta stop\n")
        r, b = jalankan("nama,nomor,setuju\nTuti,081200000332,ya\nAman,081200000500,ya\n",
                        PESAN, "--daftar-berhenti", fs)
        h = json.loads(r.stdout)
        self.assertEqual([x["nomor"] if "nomor" in x else list(x.values())[1] for x in b][:1] and len(b), 1)
        self.assertEqual(h["status"], "PERIKSA DULU")
        self.assertEqual([x["baris"] for x in h["daftar_berhenti_tidak_terbaca"]], [3])

    def test_tanpa_kolom_persetujuan_ditolak(self):
        r, _ = jalankan("nama,nomor\nA,081200000001\n")
        self.assertNotEqual(r.returncode, 0)

    def test_v108_kolom_sapaan_dipakai(self):
        k = ("Nama,No WA,Sapaan,Setuju Promo,Berhenti\nSiti Rahmawati,081234567801,Bu,ya,\n"
             "Fajar Nugroho,081234567802,pak,ya,\nRina,081234567803,,ya,\nHj. Nurul Aini,081234567804,,ya,\n"
             "Ani,081234567805,Ibu,ya,\n")
        r, b = jalankan(k, "Halo {sapaan} {nama}!\nBalas STOP untuk berhenti.\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual([x["pesan"].split("!")[0][5:] for x in b],
                         ["Bu Siti", "Pak Fajar", "Kak Rina", "Bu Nurul", "Bu Ani"])
        self.assertEqual(json.loads(r.stdout)["kolom_terdeteksi"]["sapaan"], "Sapaan")
        r, b = jalankan("nama,nomor,setuju,panggilan\nBudi,081200000001,ya,Mas\n",
                        "Halo {sapaan} {nama}!\nBalas STOP untuk berhenti.\n")
        self.assertEqual(b[0]["pesan"].split("!")[0], "Halo Mas Budi")

    def test_v108_versi_daftar_siaran_tanpa_nama_ditolak(self):
        pesan = PESAN + "---\nHalo Kak, promo roti hari ini.\nBalas STOP untuk berhenti.\n"
        r, _ = jalankan("nama,nomor,setuju\nA,081200000001,ya\n", pesan)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("daftar siaran", r.stderr)

    def test_v108_klaim_karangan_ditolak(self):
        fakta = ("Promo 1-7 Oktober: bolu pandan Rp 45.000 jadi Rp 39.000, beli 2 gratis ongkir area Bekasi Timur. "
                 "Order cukup balas chat aja. Toko Kue Bu Ani Bekasi")
        k = "nama,nomor,setuju\nA,081200000001,ya\n"
        jujur = ("Halo {sapaan} {nama}, bolu pandan Rp 39.000 (biasanya Rp 45.000), beli 2 gratis ongkir area "
                 "Bekasi Timur.\nBalas STOP untuk berhenti.")
        r, _ = jalankan(k, jujur, "--fakta", fakta)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout)["cek_klaim_terhadap_fakta"], "lulus")
        for karang in ("Yuk order, stok terbatas!", "Bolu terlaris kami.", "Dijamin halal."):
            r, _ = jalankan(k, jujur + "\n" + karang, "--fakta", fakta)
            self.assertNotEqual(r.returncode, 0, karang)
            self.assertIn("tidak disebut pemilik", r.stderr)
        r, _ = jalankan(k, jujur)
        h = json.loads(r.stdout)
        self.assertEqual(h["cek_klaim_terhadap_fakta"], "belum")
        self.assertTrue(any("--fakta-file" in x for x in h["peringatan"]))



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "siapkan_broadcast.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["--kontak", os.path.join(t, "k.csv"), "--pesan", os.path.join(t, "p.txt"), "--saya-pastikan"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60, cwd=t)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
