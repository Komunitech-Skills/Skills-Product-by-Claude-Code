#!/usr/bin/env python3
"""Tes helikopter.py pada berkas sementara. Tidak menyentuh repo nyata dan tidak mengirim apa pun.

Jalankan: python3 scripts/test_helikopter.py   (atau: python3 -m unittest discover -s scripts)
"""
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import helikopter as h  # noqa: E402


def baris(skill, jenis, status="buka", ket="x", bukti=""):
    return {"skill": skill, "jenis": jenis, "keterangan": ket, "status": status,
            "tanggal_selesai": "2026-10-15" if status == "selesai" else "", "bukti": bukti}


class TesRingkas(unittest.TestCase):
    def test_tuntas_hanya_bila_semua_selesai(self):
        b = [baris("a", "rujukan", "selesai"), baris("a", "telegram"), baris("b", "uji-ulang", "selesai")]
        r = h.ringkas(b)
        self.assertEqual(r["tuntas"], ["b"])
        self.assertEqual(r["sisa"], ["a"])
        self.assertEqual(r["per_jenis"]["telegram"], ["a"])
        self.assertEqual(r["item_buka"], 1)

    def test_tutup_dan_buka(self):
        b = [baris("a", "rujukan"), baris("a", "rujukan", ket="y")]
        self.assertEqual(h.tutup(b, "a", "rujukan", "v1.0.1", tanggal="2026-10-15"), 2)
        self.assertTrue(all(x["status"] == "selesai" and x["bukti"] == "v1.0.1" for x in b))
        with self.assertRaises(KeyError):
            h.tutup(b, "zzz", "rujukan", "-")
        self.assertEqual(h.buka(b, "a", "rujukan", "revisi ulang"), 2)
        self.assertTrue(all(x["status"] == "buka" and x["tanggal_selesai"] == "" for x in b))

    def test_tambah_tanpa_duplikat(self):
        b = []
        self.assertTrue(h.tambah(b, "a", "lain", "k"))
        self.assertFalse(h.tambah(b, "a", "lain", "k"))
        with self.assertRaises(ValueError):
            h.tambah(b, "a", "salah", "k")

    def test_baca_tulis_status(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.csv"
            h.tulis_status([baris("b", "telegram"), baris("a", "rujukan", "selesai", bukti="1.0.2")], p)
            kembali = h.baca_status(p)
            self.assertEqual([x["skill"] for x in kembali], ["a", "b"])
            self.assertEqual(kembali[0]["bukti"], "1.0.2")
            p.write_text("skill,jenis,keterangan,status,tanggal_selesai,bukti\na,aneh,k,buka,,\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                h.baca_status(p)


class TesLaporan(unittest.TestCase):
    def test_ambang_10(self):
        b = [baris(f"s{i}", "rujukan", "selesai") for i in range(9)] + [baris("t", "telegram")]
        r = h.ringkas(b)
        kirim, baru = h.perlu_kirim(r, [])
        self.assertFalse(kirim)
        self.assertEqual(len(baru), 9)
        b.append(baris("s9", "rujukan", "selesai"))
        kirim, baru = h.perlu_kirim(h.ringkas(b), [])
        self.assertTrue(kirim)
        self.assertEqual(len(baru), 10)

    def test_catat_dan_baca_laporan(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "l.md"
            b = [baris("a", "rujukan", "selesai"), baris("b", "telegram", "selesai"), baris("c", "lain")]
            r = h.ringkas(b)
            h.catat_laporan(0, "2026-10-15 10:00", r, ["a", "b"], "awal | pipa", path=p)
            lap = h.baca_laporan(p)
            self.assertEqual(len(lap), 1)
            self.assertEqual(lap[0]["baru"], ["a", "b"])
            self.assertEqual(lap[0]["tuntas"], 2)
            self.assertEqual(lap[0]["sisa"], 1)
            self.assertNotIn("|", lap[0]["catatan"])
            # setelah dilaporkan, tidak dihitung "baru" lagi
            kirim, baru = h.perlu_kirim(r, lap)
            self.assertFalse(kirim)
            self.assertEqual(baru, [])
            h.tutup(b, "c", "lain", "ok")
            kirim, baru = h.perlu_kirim(h.ringkas(b), lap)
            self.assertEqual(baru, ["c"])
            h.catat_laporan(1, "2026-10-16 10:00", h.ringkas(b), [], "", path=p)
            self.assertEqual(h.baca_laporan(p)[1]["baru"], [])


class TesPesan(unittest.TestCase):
    def test_pesan_berisi_angka_dan_tag(self):
        b = ([baris(f"tuntas{i}", "rujukan", "selesai", bukti=f"1.0.{i}") for i in range(12)]
             + [baris("x", "telegram"), baris("x", "uji-ulang"), baris("y", "telegram")])
        r = h.ringkas(b)
        kirim, baru = h.perlu_kirim(r, [])
        dt = datetime(2026, 10, 15, 9, 55, tzinfo=timezone.utc)
        p = h.susun_pesan(r, [], 1, baru, dt=dt, katalog="3 skill = 2 beta, 1 uji", catatan="router 530")
        self.assertTrue(p.startswith(h.TAG + " LAPORAN HELIKOPTER #1 — 15 Okt 2026, 09:55 UTC"))
        self.assertIn("TUNTAS: 12 skill baru — total 12 dari 14 skill antrean", p)
        self.assertIn("BELUM TUNTAS: 2 skill (3 pekerjaan)", p)
        self.assertIn("Belum tampil di bot Telegram: 2 skill (x, y)", p)
        self.assertIn("Uji ulang sebelum/sesudah: 1 skill (x)", p)
        self.assertIn("KATALOG: 3 skill = 2 beta, 1 uji.", p)
        self.assertIn("CATATAN: router 530", p)
        self.assertIn("— 1.0.0", p)

    def test_pesan_tidak_melebihi_batas_telegram(self):
        b = [baris(f"skill-nama-panjang-sekali-{i:03d}", j) for i in range(300) for j in h.JENIS]
        b += [baris(f"tuntas-nama-panjang-{i:03d}", "rujukan", "selesai", bukti="bukti " * 10) for i in range(200)]
        r = h.ringkas(b)
        _, baru = h.perlu_kirim(r, [])
        p = h.susun_pesan(r, [], 3, baru, katalog="x" * 100, catatan="y" * 100)
        self.assertLessEqual(len(p), h.BATAS_TELEGRAM)
        self.assertIn("+", p)  # daftar dipadatkan "+N lagi"

    def test_kirim_tanpa_token_gagal_tanpa_bocor(self):
        lama = os.environ.pop("tester_bot_token", None)
        try:
            with self.assertRaises(RuntimeError) as cm:
                h.kirim_telegram("uji")
            self.assertNotIn("bot", str(cm.exception).lower().replace("tester_bot_token", ""))
        finally:
            if lama is not None:
                os.environ["tester_bot_token"] = lama


if __name__ == "__main__":
    unittest.main(verbosity=1)
