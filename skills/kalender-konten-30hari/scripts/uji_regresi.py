#!/usr/bin/env python3
"""Uji regresi buat_kalender.py (+ --cek-teks/--fakta & cek_fakta.py). Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "buat_kalender.py")


def jalan(*arg):
    r = subprocess.run([sys.executable, SCRIPT] + list(arg), capture_output=True, text=True, encoding="utf-8")
    return r


def kerangka(*arg):
    r = jalan(*(list(arg) + ["--format", "json"]))
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


class Uji(unittest.TestCase):
    def test_hari_dan_tanggal(self):
        d = kerangka("--mulai", "2026-10-01", "--hari", "31")
        self.assertEqual(len(d["baris"]), 31)
        self.assertEqual(d["baris"][0]["Hari"], "Kamis")
        self.assertEqual(d["baris"][-1]["Tanggal"], "2026-10-31")

    def test_tidak_ada_promo_di_peringatan_dan_tanggal_tua(self):
        for m in ("2026-09-01", "2026-10-01", "2026-11-01", "2026-12-01"):
            for b in kerangka("--mulai", m)["baris"]:
                if "peringatan" in b["Momen"] or "Tanggal tua" in b["Momen"]:
                    self.assertNotIn("promo", b["Pilar"].lower(), (b["Tanggal"], b["Momen"]))

    def test_promo_pengguna_di_hari_peringatan_diberitahu(self):
        d = kerangka("--mulai", "2026-11-01", "--momen", "2026-11-10:Diskon 10.11:promo")
        self.assertTrue(any("Diskon 10.11" in p for p in d["ringkasan"]["peringatan"]))

    def test_isi_memeriksa_promo_di_hari_peringatan(self):
        d = kerangka("--mulai", "2026-10-01", "--hari", "7")
        d["baris"][0]["Pilar"] = "Edukasi"
        d["baris"][0]["Ide Konten"] = "Diskon 50% semua menu"
        d["baris"][0]["Momen"] = ""
        f = os.path.join(tempfile.mkdtemp(), "isi.json")
        with open(f, "w", encoding="utf-8") as h:
            json.dump(d, h)
        r = jalan("--isi", f, "--format", "json")
        hasil = json.loads(r.stdout)
        self.assertTrue(any("hari peringatan" in p for p in hasil["ringkasan"]["peringatan"]))
        self.assertIn("Kesaktian Pancasila", hasil["baris"][0]["Momen"])

    def test_input_rusak(self):
        for arg in (["--mulai", "2026-13-01"], ["--hari", "3"], ["--pilar", "Promo"], ["--momen", "2026-10-10"],
                    ["--isi", "tidak-ada.json"]):
            self.assertEqual(jalan(*arg).returncode, 1, arg)


    def tulis(self, isi, nama="teks.md"):
        f = os.path.join(tempfile.mkdtemp(), nama)
        with open(f, "w", encoding="utf-8") as h:
            h.write(isi if isinstance(isi, str) else json.dumps(isi))
        return f

    def test_ramadan_otomatis_dari_tabel_perkiraan(self):
        b = kerangka("--mulai", "2027-02-20", "--hari", "30")["baris"]
        momen = {x["Tanggal"]: x["Momen"] for x in b}
        self.assertIn("Ramadan hari ke-13", momen["2027-02-20"])
        self.assertIn("Nuzulul", momen["2027-02-24"])
        self.assertIn("THR", momen["2027-03-03"])
        self.assertIn("Idulfitri 1448 H (perkiraan", momen["2027-03-10"])
        self.assertIn("Lebaran H+1", momen["2027-03-11"])
        for x in b:  # di tengah Ramadan/Lebaran tidak ada "Tanggal tua"; Lebaran tanpa promo
            if x["Tanggal"] <= "2027-03-24":
                self.assertNotIn("Tanggal tua", x["Momen"], x["Tanggal"])
            if x["Tanggal"] in ("2027-03-10", "2027-03-11"):
                self.assertNotIn("promo", x["Pilar"].lower())

    def test_tanggal_dari_pengguna_menggantikan_tabel(self):
        b = kerangka("--mulai", "2027-02-20", "--hari", "30", "--idulfitri", "2027-03-09")["baris"]
        momen = {x["Tanggal"]: x["Momen"] for x in b}
        self.assertIn("Idulfitri", momen["2027-03-09"])
        self.assertIn("dari pengguna", momen["2027-03-09"])
        self.assertNotIn("Idulfitri", momen["2027-03-10"])

    def test_tabel_script_sama_dengan_references(self):
        sys.path.insert(0, os.path.dirname(SCRIPT))
        import buat_kalender as bk
        with open(os.path.join(os.path.dirname(SCRIPT), "..", "references", "momen-dan-pilar.md"), encoding="utf-8") as f:
            ref = f.read()
        for jenis, label in (("imlek", "Imlek"), ("awal_ramadan", "Awal Ramadan"), ("idulfitri", "Idulfitri")):
            for th, d in bk.PERKIRAAN[jenis].items():
                self.assertIn("±{} {} {}".format(d.day, bk.BULAN[d.month], th), ref, (jenis, th))

    def test_cek_teks_tanggal_idulfitri_salah_di_tips(self):
        # Kasus uji ulang OpenClaw 2026-10-01: tips menulis "19-20 Mar (Idulfitri)" padahal tabel 10 Mar 2027.
        f = self.tulis("Ramadan hari ke-13 dst.\n3. Tanggal 19-20 Mar (Idulfitri) jangan jadwalkan jualan.\n")
        r = jalan("--mulai", "2027-02-20", "--hari", "30", "--cek-teks", f)
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("19-20 Mar", r.stdout)
        f = self.tulis("Awal Ramadan ±8 Feb 2027 (perkiraan). Tanggal 10–11 Mar (Idulfitri, perkiraan) cuma ucapan;"
                       " pre-order sampai 3 Mar sebelum Lebaran.\n| 19 | 10 Mar 2027 | Rabu | Idulfitri |\n")
        r = jalan("--mulai", "2027-02-20", "--hari", "30", "--cek-teks", f)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_cek_teks_ramadan_tidak_boleh_hilang(self):
        f = self.tulis("Tips: tanggal 10 Mar Idulfitri, cuma ucapan.")
        r = jalan("--mulai", "2027-02-20", "--hari", "30", "--cek-teks", f)
        self.assertEqual(r.returncode, 2)
        self.assertIn("Ramadan", r.stdout)

    def test_isi_mengembalikan_momen_ramadan_yang_diganti(self):
        d = kerangka("--mulai", "2027-02-20", "--hari", "30")
        for x in d["baris"]:
            x["Ide Konten"], x["Hook / Judul"], x["CTA"] = "Ide", "Hook", "Order via WA"
        d["baris"][0]["Momen"] = "Tanggal tua"
        d["baris"][27]["Momen"] = "Idulfitri"          # 19 Mar, bukan Idulfitri
        r = jalan("--isi", self.tulis(d, "isi.json"), "--format", "json")
        self.assertEqual(r.returncode, 0, r.stderr)
        h = json.loads(r.stdout)
        self.assertIn("Ramadan hari ke-13", h["baris"][0]["Momen"])
        self.assertNotIn("Idulfitri", h["baris"][27]["Momen"])
        self.assertEqual(len([p for p in h["ringkasan"]["peringatan"] if "kolom Momen diganti" in p]), 2)

    def test_fakta_klaim_layanan_karangan(self):
        fakta = 'laundry kiloan "Wangi Bersih" di Depok, Rp7.000/kg, bisa antar jemput, order lewat WA.'
        f = self.tulis("CTA: jemput & antar gratis, tanpa minimal berat. Testimoni [isi: kutipan asli].")
        r = jalan("--mulai", "2026-11-01", "--cek-teks", f, "--fakta", fakta)
        self.assertEqual(r.returncode, 2)
        self.assertIn("gratis", r.stdout)
        self.assertIn("tanpa minimal", r.stdout)
        f = self.tulis("CTA: order antar jemput lewat WA. Testimoni [isi: kutipan asli].")
        self.assertEqual(jalan("--mulai", "2026-11-01", "--cek-teks", f, "--fakta", fakta).returncode, 0)
        d = kerangka("--mulai", "2026-11-01", "--hari", "7")
        for x in d["baris"]:
            x["Ide Konten"], x["Hook / Judul"], x["CTA"] = "Foto hasil cucian", "Hook", "Order via WA"
        d["baris"][2]["CTA"] = "Gratis ongkir se-Depok"
        r = jalan("--isi", self.tulis(d, "isi.json"), "--format", "json", "--fakta", fakta)
        self.assertEqual(r.returncode, 2)
        self.assertTrue(any("Baris 3" in p and "GAGAL" in p for p in json.loads(r.stdout)["ringkasan"]["peringatan"]))

    # --- Uji ulang OpenClaw 2026-10-01 (1.0.6): alur ringan + klaim produk/janji kirim karangan ---
    FAKTA_SARI = ('Tolong bikinin kalender konten 30 hari mulai 1 Maret 2027 buat usaha kue kering "Dapur Bu Sari" di '
                  'Semarang. Jualan nastar Rp95.000/toples, order lewat WA, kirim dalam kota aja. Platform IG sama '
                  'TikTok, aku sanggupnya 2 video seminggu.')
    ARG_SARI = ["--mulai", "2027-03-01", "--hari", "30", "--pilar", "Promo Nastar,Proses Dapur,Tips Kue Kering,Testimoni",
                "--platform", "IG,TikTok"]

    def isian_sari(self, ganti=None):
        baris = ["{} | {} | Foto toples nastar Rp95.000 dari dekat | Nastar Dapur Bu Sari | Order lewat WA".format(
            i, "Video IG+TikTok" if i % 4 == 0 else "Foto IG saja") for i in range(1, 31)]
        for no, teks in (ganti or {}).items():
            baris[no - 1] = teks
        return self.tulis("No | Format | Ide | Hook | CTA\n" + "\n".join(baris), "isi.txt")

    def selesai(self, isi, catatan="Tips: batch video di akhir pekan. Asumsi: gajian 25 & 1."):
        folder = tempfile.mkdtemp()
        r = jalan(*(self.ARG_SARI + ["--isi", isi, "--fakta", self.FAKTA_SARI, "--catatan", self.tulis(catatan),
                                     "--judul", "Kalender Konten Dapur Bu Sari", "--selesai", folder]))
        return r, folder

    def test_selesai_sekali_jalan_menulis_semua_file_dan_tabel_ringkas(self):
        r, folder = self.selesai(self.isian_sari())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(sorted(os.listdir(folder)), ["kalender.csv", "kalender.md", "ringkas.md"])
        tabel = [x for x in r.stdout.splitlines() if x.startswith("| ") and x[2].isdigit()]
        self.assertEqual(len(tabel), 30)                      # 1 baris per hari
        self.assertTrue(all(x.count("|") == 7 for x in tabel))  # 6 kolom saja di chat
        self.assertIn("Idulfitri 1448 H (perkiraan) — tanpa jualan", r.stdout)
        self.assertIn("Hook & CTA 3 hari pertama", r.stdout)
        self.assertIn("menunggu sidang isbat", r.stdout)
        self.assertEqual(r.stdout.count('— CTA:'), 3)
        self.assertIn("HASIL: LULUS", r.stdout)
        with open(os.path.join(folder, "kalender.csv"), encoding="utf-8-sig") as f:
            self.assertEqual(len(f.read().strip().splitlines()), 31)

    def test_selesai_menangkap_klaim_produk_dan_janji_kirim(self):
        isi = self.isian_sari({3: "3 | - | Isi nanasnya padat, bukan cuma manis doang | Renyah, lumer di mulut | "
                                   "Order via WA buat besok dikirim",
                               5: "5 | - | Bentuknya dicetak satu-satu | Pre-order Lebaran sudah dibuka | Order lewat WA",
                               13: "13 | - | Dapur Bu Sari sudah buka lagi! | Nastar fresh | Order lewat WA"})
        r, _ = self.selesai(isi)
        self.assertEqual(r.returncode, 2)
        for frasa in ("Isi nanasnya padat", "Renyah", "lumer", "besok dikirim", "dicetak satu-satu", "Pre-order",
                      "sudah buka lagi"):
            self.assertIn(frasa, r.stdout)

    def test_selesai_tanpa_fakta_gagal(self):
        """v1.0.7: --selesai tanpa --fakta/--fakta-file = GAGAL (cek karangan wajib)."""
        folder = tempfile.mkdtemp()
        r = jalan(*(self.ARG_SARI + ["--isi", self.isian_sari(), "--catatan", self.tulis("Tips: batch video."),
                                     "--selesai", folder]))
        self.assertEqual(r.returncode, 2)
        self.assertIn("--fakta-file tidak diberikan", r.stdout)
        self.assertIn("HASIL: GAGAL", r.stdout)

    def test_skill_md_aturan_wajib(self):
        """v1.0.7: SKILL.md memuat ATURAN WAJIB di awal (fakta hanya dari pengguna, ringkas default, bukan /tmp)."""
        sk = open(os.path.join(os.path.dirname(SCRIPT), "..", "SKILL.md"), encoding="utf-8").read()
        self.assertLess(sk.index("ATURAN WAJIB"), sk.index("## Tujuan"))
        for frasa in ("[isi:", "/tmp", "fakta.txt", "ringkas"):
            self.assertIn(frasa, sk.split("## Tujuan")[0])

    def selesai_arg(self, isi, *tambah):
        folder = tempfile.mkdtemp()
        return jalan(*(self.ARG_SARI + ["--isi", isi, "--fakta", self.FAKTA_SARI, "--catatan",
                                        self.tulis("Tips: batch video. Asumsi: gajian 25 & 1."),
                                        "--selesai", folder] + list(tambah)))

    def test_kapasitas_video_per_minggu_kalender(self):
        """v1.0.8: 2 video/minggu dihitung Senin-Minggu. Isian default: video tiap hari ke-4 (4, 8, 12, ...)."""
        v = "{} | Video IG+TikTok | Foto toples nastar Rp95.000 | Nastar Dapur Bu Sari | Order lewat WA"
        # Kam 4 Mar (default) + Sab 6 + Min 7 Mar = 3 video di minggu Senin 1 Mar -> GAGAL
        r = self.selesai_arg(self.isian_sari({6: v.format(6), 7: v.format(7)}), "--maks-video-minggu", "2")
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("minggu Senin 01 Mar 2027", r.stdout)
        self.assertIn("3 video", r.stdout)
        # Jum 5 + Sab 6 Mar lalu Sen 8 Mar (default): 2 per minggu kalender -> blok 7 hari dari tgl 1 tidak relevan
        r = self.selesai_arg(self.isian_sari({5: v.format(5), 6: v.format(6)}), "--maks-video-minggu", "3")
        self.assertNotIn("melebihi kemampuan", r.stdout)
        r = self.selesai_arg(self.isian_sari(), "--maks-video-minggu", "2")
        self.assertNotIn("melebihi kemampuan", r.stdout)

    def test_video_per_minggu_senin_minggu_bukan_blok_7_hari(self):
        sys.path.insert(0, os.path.dirname(SCRIPT))
        import buat_kalender as bk
        # 4 video: Kam 4, Jum 5 (minggu 1-7 Mar) dan Sen 8, Sel 9 (minggu 8-14 Mar): blok 7 hari dari tgl 1
        # tidak mengenal batas; per minggu kalender masing-masing 2 -> lolos pada maks 2.
        baris = [{"No": i, "Tanggal": "2027-03-%02d" % i, "Format": "Video"} for i in (4, 5, 8, 9)]
        self.assertEqual(bk.periksa_video(baris, 2), [])
        # Sen 8 s.d. Kam 11 = 4 video dalam satu minggu kalender (blok 7 hari dari 4 Mar juga akan menangkap, tapi
        # Kam 11-Rab 17 tidak): harus GAGAL.
        baris = [{"No": i, "Tanggal": "2027-03-%02d" % i, "Format": "Video"} for i in (9, 11, 12, 14)]
        self.assertEqual(len(bk.periksa_video(baris, 2)), 1)

    def test_label_ramadan_h_n_ditolak(self):
        isi = self.isian_sari({2: "2 | - | Persiapan | Ramadan H-22 di Dapur Bu Sari | Order lewat WA"})
        r = self.selesai_arg(isi)
        self.assertEqual(r.returncode, 2)
        self.assertIn("Ramadan hari ke-N", r.stdout)
        f = self.tulis("Tips: saat Ramadan H-22 siapkan stok.")
        r = jalan(*(self.ARG_SARI + ["--cek-teks", f]))
        self.assertEqual(r.returncode, 2)
        self.assertIn("Ramadan hari ke-N", r.stdout)

    def test_selesai_cek_tanggal_di_catatan(self):
        r, _ = self.selesai(self.isian_sari(), "Tips: Idulfitri ±19 Mar 2027 jangan jualan.")
        self.assertEqual(r.returncode, 2)
        self.assertIn("19 Mar 2027", r.stdout)

    def test_kalimat_edukasi_rasa_bukan_klaim(self):
        f = self.tulis("Tips simpan nastar biar tetap renyah: toples rapat. Jadwal produksi padat minggu ini.")
        r = jalan(*(self.ARG_SARI + ["--cek-teks", f, "--fakta", self.FAKTA_SARI]))
        self.assertNotIn("[fakta]", r.stdout)

    def test_isian_teks_rusak(self):
        for isi in ("1 | a | b", "x | a | b | c", "31 | a | b | c"):
            r = jalan(*(self.ARG_SARI + ["--isi", self.tulis(isi, "isi.txt"), "--format", "md"]))
            self.assertEqual(r.returncode, 1, isi)
        r = jalan("--isi", self.tulis("1 | a | b | c", "isi.txt"), "--format", "md")  # tanpa --mulai
        self.assertEqual(r.returncode, 1)

    def test_format_ringkas_kerangka(self):
        r = jalan(*(self.ARG_SARI + ["--format", "ringkas"]))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len([x for x in r.stdout.splitlines() if x.startswith("| ") and x[2].isdigit()]), 30)
        self.assertNotIn("menunggu sidang isbat", r.stdout)  # label dipendekkan → hemat token


if __name__ == "__main__":
    unittest.main(verbosity=2)
