#!/usr/bin/env python3
"""Uji regresi bot-trading-kripto (Python standar, tanpa jaringan).

  python3 tests/uji_regresi.py        (Windows: python / py)

Mencakup: tanda tangan HMAC (vektor dari dokumentasi resmi), validasi konfigurasi, matematika
strategi (DCA/grid/TP-SL/rebalancing), isi order + fee + PPh (Decimal), batas risiko,
tombol berhenti, gerbang mode live, pemeriksaan izin kunci, penyamaran kunci di log,
backtest pada data asli, dan alur penuh testnet/live terhadap SERVER TIRUAN lokal
(tests/mock_bursa.py) -- bukan bursa sungguhan.
"""

import contextlib
import copy
import csv
import io
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from decimal import Decimal as D

SINI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(SINI)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
sys.path.insert(0, SINI)

import inti  # noqa: E402
import bursa  # noqa: E402
import backtest  # noqa: E402
import berhenti  # noqa: E402
import hitung_pajak_biaya  # noqa: E402
import jalankan_bot  # noqa: E402
import siapkan_live  # noqa: E402
import mock_bursa  # noqa: E402

WIB = inti.WIB
T0 = datetime(2026, 9, 29, 8, 0, tzinfo=WIB)

_HOME_ASLI = {}


def setUpModule():
    """Tombol berhenti global ditulis ke ~/.komunitech/...; selama uji, 'home' dialihkan ke folder
    sementara supaya uji tidak pernah menulis ke home pengguna sungguhan."""
    global HOME_UJI
    HOME_UJI = tempfile.mkdtemp(prefix="uji-bot-home-")
    for k in ("HOME", "USERPROFILE"):
        _HOME_ASLI[k] = os.environ.get(k)
        os.environ[k] = HOME_UJI


def tearDownModule():
    for k, v in _HOME_ASLI.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    shutil.rmtree(HOME_UJI, ignore_errors=True)

DASAR = {
    "mode": "paper", "bursa": "indodax", "pasangan": "btc_idr",
    "strategi": {"jenis": "dca", "nominal_per_beli": "100000", "interval_jam": 24},
    "batas_risiko": {"modal_maks_per_order": "100000", "modal_maks_total": "1000000",
                     "stop_loss_persen": "20", "rugi_harian_maks": "200000", "order_terbuka_maks": 2},
    "biaya": {"fee_persen": "0.2", "pajak": "domestik"},
}


def cfg_dari(**ubah):
    c = copy.deepcopy(DASAR)
    for k, v in ubah.items():
        c[k] = v
    return inti.normalisasi_konfigurasi(c)


def jalankan(fungsi, argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        kode = fungsi(argv)
    return kode, buf.getvalue()


class TandaTangan(unittest.TestCase):
    def test_binance_vektor_docs(self):
        q = "symbol=LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559"
        self.assertEqual(bursa.Binance.tanda_tangan(mock_bursa.BINANCE_SECRET, q),
                         "c8db56825ae71d6d79447849e617115f4a920fa2acdcab2b053c4b2838bd6b71")

    def test_indodax_vektor_docs(self):
        body = "method=getInfo&timestamp=1578304294000&recvWindow=1578303937000"
        self.assertEqual(bursa.Indodax.tanda_tangan(mock_bursa.INDODAX_SECRET, body),
                         "bab004e5a518740d7a33b38b44dbebecd3fb39f40b42391af39fcce06edabff5233b3e8064a07c528d1c751a6923d5116026c7786e01b22e2d35277a098cae99")


class Konfigurasi(unittest.TestCase):
    def gagal(self, pesan_potongan, **ubah):
        with self.assertRaises(inti.KonfigurasiTidakValid) as cm:
            cfg_dari(**ubah)
        self.assertIn(pesan_potongan, str(cm.exception))

    def test_tanpa_batas_risiko_ditolak(self):
        self.gagal("batas_risiko", batas_risiko=None)

    def test_batas_tidak_lengkap(self):
        br = dict(DASAR["batas_risiko"]); del br["rugi_harian_maks"]
        self.gagal("rugi_harian_maks", batas_risiko=br)

    def test_float_ditolak(self):
        br = dict(DASAR["batas_risiko"], modal_maks_total=1000000.5)
        self.gagal("tulis sebagai teks", batas_risiko=br)

    def test_per_order_lebih_besar_dari_total(self):
        br = dict(DASAR["batas_risiko"], modal_maks_per_order="2000000")
        self.gagal("tidak boleh lebih besar", batas_risiko=br)

    def test_nominal_dca_melebihi_per_order(self):
        self.gagal("melebihi", strategi={"jenis": "dca", "nominal_per_beli": "150000", "interval_jam": 24})

    def test_grid_melebihi_modal_total(self):
        self.gagal("melebihi modal_maks_total", strategi={"jenis": "grid", "harga_bawah": "1", "harga_atas": "2",
                                                          "jumlah_grid": 20, "nominal_per_grid": "100000"})

    def test_live_binance_perlu_pernyataan(self):
        self.gagal("PAKD", mode="live", bursa="binance", pasangan="BTCUSDT", koin="BTC", kutipan="USDT",
                   kunci={"env": True})

    def test_live_tanpa_pajak_ditolak(self):
        self.gagal("tidak_dihitung", mode="live", kunci={"env": True}, biaya={"pajak": "tidak_dihitung"})

    def test_testnet_perlu_kunci(self):
        self.gagal("kunci", mode="testnet")

    def test_pasangan_indodax(self):
        self.gagal("_idr", pasangan="BTCIDR")

    def test_default_fee_pajak(self):
        c = cfg_dari(biaya={})
        self.assertEqual(c["_d"]["fee_persen"], D("0.2"))
        self.assertEqual(c["_d"]["tarif_pph"], D("0.0021"))


class IsiOrderPajak(unittest.TestCase):
    def test_beli_tidak_melebihi_nominal(self):
        c = cfg_dari()
        isi = inti.simulasi_isi(c, "beli", D("1503453000"), D("100000"))
        self.assertLessEqual(isi["bersih"], D("100000"))
        self.assertEqual(isi["fee"], (isi["bruto"] * D("0.002")).quantize(D("1"), rounding="ROUND_HALF_UP"))

    def test_pph_dibulatkan_ke_bawah(self):
        c = cfg_dari()
        # 0,21% x 999.999 = 2.099,9979 -> 2.099 (tidak pernah melebihi tarif)
        isi = inti.simulasi_isi(c, "jual", D("999999"), jumlah_koin=D("1"))
        self.assertEqual(isi["pajak"], D("2099"))
        self.assertEqual(isi["fee"], D("2000"))
        self.assertEqual(isi["bersih"], D("999999") - D("2000") - D("2099"))

    def test_luar_negeri_1_persen(self):
        c = cfg_dari(biaya={"fee_persen": "0", "pajak": "luar_negeri"})
        self.assertEqual(inti.simulasi_isi(c, "jual", D("15000000"), jumlah_koin=D("1"))["pajak"], D("150000"))

    def test_realized_pl_rata_rata(self):
        c = cfg_dari(biaya={"fee_persen": "0", "pajak": "tidak_dihitung"})
        st = inti.state_awal(c)
        for h in ("100", "200"):
            inti.terapkan_isi(st, inti.simulasi_isi(c, "beli", D(h), D("100")), "IDR")
        self.assertEqual(D(st["posisi_koin"]), D("1.5"))
        pl = inti.terapkan_isi(st, inti.simulasi_isi(c, "jual", D("300"), jumlah_koin=D("1.5")), "IDR")
        self.assertEqual(pl, D("250"))  # jual 450 - modal 200
        self.assertEqual(D(st["kas"]), D("1000000") - 200 + 450)

    def test_skrip_pajak(self):
        kode, out = jalankan(hitung_pajak_biaya.main, ["--nilai-jual", "15000000", "--pajak", "domestik", "--fee-persen", "0.2"])
        j = json.loads(out)
        self.assertEqual((kode, j["pph"], j["fee"], j["diterima_bersih"]), (0, 31500, 30000, 14938500))
        self.assertIn("Coretax", j["catatan"])

    def test_skrip_pajak_input_buruk(self):
        kode, out = jalankan(hitung_pajak_biaya.main, ["--nilai-jual", "abc"])
        self.assertEqual(kode, 1)


class Strategi(unittest.TestCase):
    def test_dca_interval(self):
        c = cfg_dari()
        st = inti.state_awal(c)
        n = inti.rencanakan(c, st, D("100"), T0)
        self.assertEqual([x["sisi"] for x in n], ["beli"])
        st["terakhir_beli_dca"] = T0.isoformat()
        self.assertEqual(inti.rencanakan(c, st, D("100"), T0 + timedelta(hours=23)), [])
        self.assertEqual(len(inti.rencanakan(c, st, D("100"), T0 + timedelta(hours=24))), 1)

    def test_dca_take_profit(self):
        c = cfg_dari(strategi={"jenis": "dca", "nominal_per_beli": "100000", "interval_jam": 24, "take_profit_persen": "10"})
        st = inti.state_awal(c)
        st.update(posisi_koin="1", biaya_perolehan="100", terakhir_beli_dca=T0.isoformat())
        self.assertEqual(inti.rencanakan(c, st, D("109.99"), T0), [])
        self.assertEqual(inti.rencanakan(c, st, D("110"), T0)[0]["sisi"], "jual")

    def test_grid_level_dan_siklus(self):
        c = cfg_dari(strategi={"jenis": "grid", "harga_bawah": "100", "harga_atas": "200", "jumlah_grid": 4,
                               "nominal_per_grid": "100000"},
                     biaya={"fee_persen": "0", "pajak": "tidak_dihitung"})
        self.assertEqual(inti.level_grid(c["_d"]), [D(100), D(125), D(150), D(175), D(200)])
        st = inti.state_awal(c)
        n = inti.rencanakan(c, st, D("130"), T0)
        self.assertEqual((n[0]["sisi"], n[0]["slot"]), ("beli", "1"))
        isi = inti.simulasi_isi(c, "beli", D("130"), D("100000"))
        inti.terapkan_isi(st, isi, "IDR"); inti.catat_niat_berhasil(st, n[0], isi, T0)
        self.assertEqual(inti.rencanakan(c, st, D("140"), T0), [])        # pita sama, slot terisi
        n2 = inti.rencanakan(c, st, D("150"), T0)
        self.assertEqual([(x["sisi"], x["slot"]) for x in n2], [("jual", "1"), ("beli", "2")])
        self.assertEqual(inti.rencanakan(c, inti.state_awal(c), D("90"), T0), [])   # di bawah rentang
        self.assertEqual(inti.rencanakan(c, inti.state_awal(c), D("200"), T0), [])  # di atas rentang

    def test_tp_sl(self):
        c = cfg_dari(strategi={"jenis": "tp_sl", "nominal_beli": "100000", "take_profit_persen": "15",
                               "stop_loss_persen": "8", "harga_masuk_maks": "100"})
        st = inti.state_awal(c)
        self.assertEqual(inti.rencanakan(c, st, D("101"), T0), [])
        self.assertTrue(inti.rencanakan(c, st, D("100"), T0)[0]["tp_sl_masuk"])
        st.update(posisi_koin="1", biaya_perolehan="100", tp_sl_status="dalam_posisi")
        self.assertEqual(inti.rencanakan(c, st, D("114.9"), T0), [])
        self.assertIn("take-profit", inti.rencanakan(c, st, D("115"), T0)[0]["alasan"])
        self.assertIn("stop-loss", inti.rencanakan(c, st, D("92"), T0)[0]["alasan"])
        st.update(posisi_koin="0", biaya_perolehan="0", tp_sl_status="selesai")
        self.assertEqual(inti.rencanakan(c, st, D("50"), T0), [])  # tidak masuk ulang otomatis

    def test_rebalancing(self):
        c = cfg_dari(strategi={"jenis": "rebalancing", "target_persen_koin": "50", "ambang_deviasi_persen": "5"},
                     batas_risiko=dict(DASAR["batas_risiko"], modal_maks_per_order="1000000"))
        st = inti.state_awal(c)
        n = inti.rencanakan(c, st, D("100"), T0)
        self.assertEqual((n[0]["sisi"], n[0]["nilai_kutipan"]), ("beli", D("500000")))
        st.update(kas="500000", posisi_koin="5000", biaya_perolehan="500000")   # 50:50
        self.assertEqual(inti.rencanakan(c, st, D("100"), T0), [])
        n = inti.rencanakan(c, st, D("125"), T0)   # koin 625rb dari 1,125jt = 55,56%
        self.assertEqual(n[0]["sisi"], "jual")
        self.assertEqual((n[0]["jumlah_koin"] * D("125")).quantize(D("1")), D("62500"))


class Risiko(unittest.TestCase):
    def test_stop_loss_global(self):
        c = cfg_dari()
        st = inti.state_awal(c); st.update(posisi_koin="1", biaya_perolehan="100", kas="999900")
        self.assertEqual(inti.cek_risiko_awal(c, st, D("80.01"), T0), (None, None))
        alasan, paksa = inti.cek_risiko_awal(c, st, D("80"), T0)
        self.assertIn("STOP-LOSS", alasan)
        self.assertEqual((paksa["sisi"], paksa["jumlah_koin"]), ("jual", D("1")))

    def test_rugi_harian(self):
        c = cfg_dari(batas_risiko=dict(DASAR["batas_risiko"], stop_loss_persen="90"))
        st = inti.state_awal(c); st.update(posisi_koin="10", biaya_perolehan="1000000", kas="0")
        self.assertEqual(inti.cek_risiko_awal(c, st, D("100000"), T0)[0], None)
        self.assertEqual(inti.cek_risiko_awal(c, st, D("80000"), T0 + timedelta(hours=2))[0], None)   # rugi 200rb = batas
        self.assertIn("RUGI HARIAN", inti.cek_risiko_awal(c, st, D("79999"), T0 + timedelta(hours=3))[0])
        # hari baru: patokan = nilai putaran terakhir sebelum pergantian hari
        st2 = inti.state_awal(c); st2.update(posisi_koin="10", biaya_perolehan="1000000", kas="0")
        inti.cek_risiko_awal(c, st2, D("100000"), T0)
        self.assertIn("RUGI HARIAN", inti.cek_risiko_awal(c, st2, D("70000"), T0 + timedelta(days=1))[0])

    def test_batas_modal_dan_order_terbuka(self):
        c = cfg_dari()
        st = inti.state_awal(c)
        niat = {"sisi": "beli", "nilai_kutipan": D("100000")}
        self.assertEqual(inti.cek_niat(c, st, niat, D("100"), 0)[0], "ok")
        self.assertEqual(inti.cek_niat(c, st, {"sisi": "beli", "nilai_kutipan": D("100001")}, D("100"), 0)[0], "berhenti")
        st["biaya_perolehan"] = "950000"
        s, p = inti.cek_niat(c, st, niat, D("100"), 0)
        self.assertEqual(s, "berhenti"); self.assertIn("MODAL TOTAL", p)
        s, p = inti.cek_niat(c, inti.state_awal(c), niat, D("100"), 2)
        self.assertEqual(s, "berhenti"); self.assertIn("ORDER TERBUKA", p)
        self.assertEqual(inti.cek_niat(c, inti.state_awal(c), {"sisi": "beli", "nilai_kutipan": D("5000")}, D("100"), 0)[0], "lewati")


class Folder(unittest.TestCase):
    """Tes yang butuh folder bot sementara (di luar repo git)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji-bot-")
        self.bot = os.path.join(self.tmp, "bot")
        os.makedirs(self.bot)
        self.cfgp = os.path.join(self.bot, "konfigurasi.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        shutil.rmtree(inti.folder_stop_global(), ignore_errors=True)
        os.environ.pop(bursa.ENV_KUNCI, None); os.environ.pop(bursa.ENV_SECRET, None)

    def suntik_bukti_paper(self, jam=25, putaran=3):
        """Tiru bukti paper dengan harga asli (uji tidak boleh menunggu 24 jam sungguhan)."""
        cfg = inti.muat_konfigurasi(self.cfgp)
        st = self.state()
        sj = inti.sidik_jari_strategi(cfg)
        akhir = datetime.now(WIB)
        st.setdefault("paper_nyata_per_sidik", {})[sj] = {
            "jumlah": putaran, "pertama": (akhir - timedelta(hours=jam)).isoformat(timespec="seconds"),
            "terakhir": akhir.isoformat(timespec="seconds")}
        with open(os.path.join(self.bot, "state.json"), "w") as f:
            json.dump(st, f)

    def tulis_cfg(self, c):
        with open(self.cfgp, "w") as f:
            json.dump(c, f)

    def tulis_kunci(self, k, s, izin=0o600):
        p = os.path.join(self.tmp, "kunci.json")
        with open(p, "w") as f:
            json.dump({"api_key": k, "api_secret": s}, f)
        os.chmod(p, izin)
        return p

    def tick(self, *extra):
        return jalankan(jalankan_bot.main, ["--konfigurasi", self.cfgp, *extra])

    def state(self):
        with open(os.path.join(self.bot, "state.json")) as f:
            return json.load(f)


class AlurPaper(Folder):
    def test_paper_dca_lalu_tombol_berhenti(self):
        self.tulis_cfg(DASAR)
        kode, out = self.tick("--harga", "1500000000", "--sekarang", T0.isoformat())
        self.assertEqual(kode, 2); self.assertIn("BELI", out); self.assertIn("[SIMULASI", out)
        self.assertIn("bukan nasihat investasi", out.lower())
        kode, out = self.tick("--harga", "1500000000", "--sekarang", (T0 + timedelta(hours=1)).isoformat())
        self.assertEqual((kode, out.strip()), (0, "NO_REPLY"))
        # tombol berhenti
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp])
        self.assertTrue(os.path.exists(os.path.join(self.bot, "STOP")))
        kode, out = self.tick("--harga", "1500000000", "--sekarang", (T0 + timedelta(days=2)).isoformat())
        self.assertEqual(kode, 3); self.assertIn("Tombol berhenti", out); self.assertNotIn("BELI", out)
        kode, out = self.tick("--harga", "1500000000", "--sekarang", (T0 + timedelta(days=3)).isoformat())
        self.assertEqual(out.strip(), "NO_REPLY")   # notifikasi berhenti hanya sekali
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan"])
        self.assertEqual(kode, 1)                   # wajib --saya-sudah-cek
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        self.assertEqual(kode, 0); self.assertFalse(os.path.exists(os.path.join(self.bot, "STOP")))
        kode, out = self.tick("--harga", "1500000000", "--sekarang", (T0 + timedelta(days=4)).isoformat())
        self.assertIn("BELI", out)

    def test_stop_loss_menjual_lalu_berhenti(self):
        self.tulis_cfg(DASAR)
        self.tick("--harga", "1000000", "--sekarang", T0.isoformat())
        kode, out = self.tick("--harga", "790000", "--sekarang", (T0 + timedelta(hours=1)).isoformat())
        self.assertEqual(kode, 3); self.assertIn("JUAL", out); self.assertIn("STOP-LOSS", out)
        st = self.state()
        self.assertTrue(st["berhenti"]); self.assertEqual(D(st["posisi_koin"]), 0)
        kode, out = self.tick("--harga", "790000", "--sekarang", (T0 + timedelta(days=2)).isoformat())
        self.assertEqual(out.strip(), "NO_REPLY")

    def test_openclaw_selalu_exit_0(self):
        self.tulis_cfg(dict(DASAR, batas_risiko=None))
        kode, out = self.tick("--openclaw")
        self.assertEqual(kode, 0); self.assertIn("konfigurasi bermasalah", out)
        self.tulis_cfg(DASAR)
        kode, out = self.tick("--openclaw", "--harga", "1500000000", "--sekarang", T0.isoformat())
        self.assertEqual(kode, 0); self.assertIn("BELI", out)

    def test_perubahan_aturan_saat_pegang_koin(self):
        self.tulis_cfg(DASAR)
        self.tick("--harga", "1000000", "--sekarang", T0.isoformat())
        c = copy.deepcopy(DASAR); c["strategi"]["interval_jam"] = 12
        self.tulis_cfg(c)
        kode, out = self.tick("--harga", "1000000", "--sekarang", (T0 + timedelta(hours=1)).isoformat())
        self.assertEqual(kode, 3); self.assertIn("berubah", out)

    def test_harga_manual_hanya_paper(self):
        self.tulis_cfg(dict(DASAR, mode="testnet", kunci={"env": True}))
        kode, out = self.tick("--harga", "1")
        self.assertEqual(kode, 1)


class Kunci(Folder):
    def test_izin_file_terbuka_ditolak(self):
        if os.name != "posix":
            self.skipTest("izin file POSIX")
        p = self.tulis_kunci("abcdefgh", "ijklmnop", 0o644)
        with self.assertRaises(bursa.ErrorKunci) as cm:
            bursa.muat_kunci({"kunci": {"file": p}}, SKILL)
        self.assertIn("chmod 600", str(cm.exception))

    def test_kunci_di_repo_git_ditolak(self):
        os.makedirs(os.path.join(self.tmp, ".git"))
        p = self.tulis_kunci("abcdefgh", "ijklmnop")
        with self.assertRaises(bursa.ErrorKunci) as cm:
            bursa.muat_kunci({"kunci": {"file": p}}, SKILL)
        self.assertIn("repo git", str(cm.exception))

    def test_kunci_di_folder_skill_ditolak(self):
        with self.assertRaises(bursa.ErrorKunci):
            bursa.muat_kunci({"kunci": {"file": os.path.join(SKILL, "templates", "kunci-contoh.json")}}, SKILL)

    def test_repr_menyembunyikan(self):
        k = bursa.Kunci("RAHASIA-KEY-123", "RAHASIA-SECRET-456", "uji")
        self.assertNotIn("RAHASIA", repr(k) + str(k) + f"{k}")

    def test_penyamar(self):
        p = inti.Penyamar(["RAHASIA-SECRET-456"])
        self.assertNotIn("RAHASIA", p("x RAHASIA-SECRET-456 y"))
        self.assertIn("signature=***", p("a?signature=c8db56825ae71d6d79447849e617115f"))

    def test_url_uji_hanya_localhost(self):
        with self.assertRaises(ValueError):
            bursa._periksa_url_uji("https://penipu.example.com")


class AlurMock(Folder):
    """Alur penuh testnet/live terhadap server tiruan lokal (bukan bursa sungguhan)."""

    @classmethod
    def setUpClass(cls):
        cls.url, cls.k, cls.srv = mock_bursa.jalankan()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        super().setUp()
        k = self.k
        k.withdraw_aktif, k.order_terbuka, k.putus_saat_order, k.tolak_order = False, 0, False, None
        k.alihkan_ke, k.harga_btcusdt = None, D("60000")
        k.permintaan.clear(); k.order.clear()

    def cfg_binance(self, mode, **ubah):
        c = {"mode": mode, "bursa": "binance", "pasangan": "BTCUSDT", "koin": "BTC", "kutipan": "USDT",
             "strategi": {"jenis": "dca", "nominal_per_beli": "100", "interval_jam": 24},
             "batas_risiko": {"modal_maks_per_order": "100", "modal_maks_total": "1000", "stop_loss_persen": "20",
                              "rugi_harian_maks": "100", "order_terbuka_maks": 2},
             "biaya": {"fee_persen": "0.1", "pajak": "luar_negeri"},
             "kunci": {"file": self.tulis_kunci(mock_bursa.BINANCE_KEY, mock_bursa.BINANCE_SECRET)}}
        c.update(ubah)
        return c

    def semua_teks(self):
        teks = ""
        for n in os.listdir(self.bot):
            with open(os.path.join(self.bot, n), encoding="utf-8", errors="ignore") as f:
                teks += f.read()
        return teks

    def test_testnet_binance_order_bertanda_tangan(self):
        self.tulis_cfg(self.cfg_binance("testnet"))
        kode, out = self.tick("--url-uji", self.url)
        self.assertEqual(kode, 2, out); self.assertIn("[TESTNET", out); self.assertIn("BELI", out)
        post = [r for r in self.k.permintaan if r[0] == "POST"]
        self.assertEqual(len(post), 1)
        # BTCUSDT = swap kripto-kripto: PPh 1% sisi beli disisihkan -> 100 / 1,01 = 99,00 USDT
        self.assertIn("type=MARKET", post[0][3]); self.assertIn("quoteOrderQty=99.00", post[0][3])
        # rahasia tidak pernah muncul di query, log, state, transaksi, atau keluaran
        for r in self.k.permintaan:
            self.assertNotIn(mock_bursa.BINANCE_SECRET, r[3] + r[4])
        self.assertNotIn(mock_bursa.BINANCE_SECRET, self.semua_teks() + out)
        self.assertNotIn(mock_bursa.BINANCE_KEY, self.semua_teks() + out)
        st = self.state()
        self.assertEqual(D(st["posisi_koin"]), D("0.00165") - D("0.00000165"))  # komisi dipotong dari BTC
        self.assertEqual(D(st["total_pajak"]), D("0.99"))                        # 1% x 99 USDT diserahkan
        self.assertLessEqual(D(st["biaya_perolehan"]), D("100"))

    def test_live_binance_gerbang_bertahap(self):
        c = self.cfg_binance("paper")
        self.tulis_cfg(c)
        c_live = dict(c, mode="live", saya_paham_binance_bukan_pakd_ojk=True)
        # 1) live tanpa bukti simulasi -> ditolak
        self.tulis_cfg(c_live)
        kode, out = self.tick("--url-uji", self.url, "--izinkan-live")
        self.assertEqual(kode, 3); self.assertIn("belum pernah dijalankan di mode simulasi", out)
        shutil.rmtree(self.bot); os.makedirs(self.bot)
        # 2) simulasi dulu -- satu putaran lewat server tiruan BELUM cukup (L4)
        self.tulis_cfg(c)
        kode, out = self.tick("--url-uji", self.url)
        self.assertEqual(kode, 2, out)
        self.tulis_cfg(c_live)
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp])
        self.assertEqual(kode, 2); self.assertIn("BELUM CUKUP", out)
        self.suntik_bukti_paper()
        # 3) live tanpa konfirmasi
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp])
        self.assertEqual(kode, 0); self.assertIn("SAYA TANGGUNG RISIKONYA", out)
        self.assertIn("DAFTAR PERIKSA WAJIB", out); self.assertIn("Enable Withdrawals", out)
        kode_konf = inti.sidik_jari_penuh(inti.muat_konfigurasi(self.cfgp))
        frasa = f"LIVE {kode_konf} SAYA TANGGUNG RISIKONYA"
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--frasa", "LIVE salah SAYA TANGGUNG RISIKONYA",
                                                 "--saya-sudah-cek-tanpa-withdraw"])
        self.assertEqual(kode, 2)
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--frasa", frasa])
        self.assertEqual(kode, 2)   # tanpa pernyataan tanpa-withdraw
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--frasa", frasa,
                                                 "--saya-sudah-cek-tanpa-withdraw"])
        self.assertEqual(kode, 0, out)
        # 4) tanpa --izinkan-live tetap ditolak
        kode, out = self.tick("--url-uji", self.url)
        self.assertEqual(kode, 3); self.assertIn("--izinkan-live", out)
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        # 5) kunci dengan izin withdraw -> ditolak
        self.k.withdraw_aktif = True
        kode, out = self.tick("--url-uji", self.url, "--izinkan-live")
        self.assertEqual(kode, 3); self.assertIn("withdraw", out)
        self.assertEqual([r for r in self.k.permintaan if r[0] == "POST"], [])
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        # 6) kunci benar -> order live (ke server tiruan)
        self.k.withdraw_aktif = False
        kode, out = self.tick("--url-uji", self.url, "--izinkan-live")
        self.assertEqual(kode, 2, out); self.assertIn("[LIVE", out); self.assertIn("BELI", out)
        # 7) konfigurasi diubah -> konfirmasi tidak berlaku
        c2 = copy.deepcopy(c_live); c2["batas_risiko"]["rugi_harian_maks"] = "150"
        self.tulis_cfg(c2)
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        kode, out = self.tick("--url-uji", self.url, "--izinkan-live")
        self.assertEqual(kode, 3); self.assertIn("simulasi", out)  # sidik strategi berubah -> bukti simulasi lama tidak berlaku

    def test_order_putus_berhenti(self):
        self.tulis_cfg(self.cfg_binance("testnet"))
        self.k.putus_saat_order = True
        kode, out = self.tick("--url-uji", self.url)
        self.assertEqual(kode, 3); self.assertIn("TIDAK PASTI", out); self.assertIn("cek manual", out.lower())

    def test_order_terbuka_melebihi_batas(self):
        self.tulis_cfg(self.cfg_binance("testnet"))
        self.k.order_terbuka = 2
        kode, out = self.tick("--url-uji", self.url)
        self.assertEqual(kode, 3); self.assertIn("ORDER TERBUKA", out)
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--batalkan-order", "--url-uji", self.url])
        self.assertIn("dibatalkan: 2", out)

    def test_order_ditolak_bursa(self):
        self.tulis_cfg(self.cfg_binance("testnet"))
        self.k.tolak_order = "Account has insufficient balance for requested action."
        kode, out = self.tick("--url-uji", self.url)
        self.assertEqual(kode, 3); self.assertIn("insufficient balance", out)

    def test_indodax_testnet_via_mock(self):
        c = copy.deepcopy(DASAR)
        c.update(mode="testnet", kunci={"file": self.tulis_kunci(mock_bursa.INDODAX_KEY, mock_bursa.INDODAX_SECRET)})
        self.tulis_cfg(c)
        kode, out = self.tick("--url-uji", self.url)
        self.assertEqual(kode, 2, out); self.assertIn("BELI", out)
        body = [r[4] for r in self.k.permintaan if r[1] == "/tapi" and "method=trade" in r[4]][0]
        self.assertIn("order_type=market", body); self.assertIn("idr=100000", body)
        self.assertNotIn(mock_bursa.INDODAX_SECRET, self.semua_teks() + out)

    def test_kunci_salah_ditolak_mock(self):
        c = self.cfg_binance("testnet")
        c["kunci"] = {"file": self.tulis_kunci(mock_bursa.BINANCE_KEY, "secret-salah-12345")}
        self.tulis_cfg(c)
        kode, out = self.tick("--url-uji", self.url)
        self.assertIn("Signature", out)
        self.assertEqual([r for r in self.k.permintaan if r[0] == "POST"], [])


class Backtest(unittest.TestCase):
    CSV = os.path.join(SINI, "data", "btcidr-harian-2025-2026.csv")

    def test_backtest_data_asli(self):
        c = cfg_dari(strategi={"jenis": "dca", "nominal_per_beli": "100000", "interval_jam": 168})
        data, rusak = backtest.baca_csv(self.CSV)
        self.assertGreater(len(data), 300); self.assertEqual(rusak, [])
        h = backtest.jalankan(c, data)
        # ekuitas = kas + koin x harga akhir (konsisten)
        self.assertGreater(h["jumlah_transaksi"], 0)
        self.assertEqual(D(h["total_fee"]), sum(D(t["fee"]) for t in h["transaksi"]))
        self.assertEqual(D(h["total_pph"]), sum(D(t["pph"]) for t in h["transaksi"]))
        # verifikasi independen: kas akhir = modal - total bayar beli + total terima jual
        kas = D(h["modal_awal_bot"]) - sum(D(t["bersih"]) for t in h["transaksi"] if t["sisi"] == "beli") \
            + sum(D(t["bersih"]) for t in h["transaksi"] if t["sisi"] == "jual")
        self.assertEqual(kas, D(h["kas_tersisa"]))
        # PPh tiap jual = floor(0,21% x bruto) -> tidak pernah melebihi tarif
        for t in h["transaksi"]:
            if t["sisi"] == "jual":
                bruto = D(t["bersih"]) + D(t["fee"]) + D(t["pph"])
                self.assertLessEqual(D(t["pph"]), bruto * D("0.0021"))
                self.assertGreater(D(t["pph"]) + 1, bruto * D("0.0021"))

    def test_csv_rusak(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("tanggal;close\n2026-01-01;100\n2026-01-02;abc\nxx;5\n2026-01-03;110\n")
        data, rusak = backtest.baca_csv(f.name)
        os.remove(f.name)
        self.assertEqual((len(data), [r["baris"] for r in rusak]), (2, [3, 4]))


# =============================================================================== revisi 1.0.1
CFG_H1 = {
    "mode": "paper", "bursa": "indodax", "pasangan": "btc_idr",
    "strategi": {"jenis": "dca", "nominal_per_beli": "1000000", "interval_jam": 24},
    "batas_risiko": {"modal_maks_per_order": "1000000", "modal_maks_total": "2000000",
                     "stop_loss_persen": "50", "rugi_harian_maks": "100000", "order_terbuka_maks": 2},
    "biaya": {"fee_persen": "0.2", "pajak": "domestik"},
}


class H1JamMundur(Folder):
    """H1: batas rugi harian tidak boleh ter-reset oleh jam sistem yang mundur."""

    def tick_pada(self, harga, waktu):
        return self.tick("--harga", harga, "--sekarang", waktu)

    def test_reproduksi_penguji_rugi_155022_berhenti(self):
        self.tulis_cfg(CFG_H1)
        # 1/10 08.00: beli Rp1 jt (0,000998 BTC @ Rp1 M), patokan hari = Rp2.000.000
        kode, out = self.tick_pada("1000000000", "2026-10-01T08:00:00+07:00")
        self.assertIn("BELI", out)
        # 1/10 10.00: rugi Rp81.836 (< batas Rp100.000) -> tidak berhenti
        kode, out = self.tick_pada("920000000", "2026-10-01T10:00:00+07:00")
        self.assertNotEqual(kode, 3, out)
        self.assertEqual(self.state()["buku_rugi_harian"]["2026-10-01"], "2000000")
        # jam komputer MUNDUR ke 30/9 -> tanggal tetap 1/10, patokan tidak diganti, peringatan dikirim
        kode, out = self.tick_pada("920000000", "2026-09-30T12:00:00+07:00")
        self.assertNotEqual(kode, 3, out)
        self.assertIn("jam komputer mundur", out)
        st = self.state()
        self.assertEqual((st["hari"], st["ekuitas_awal_hari"]), ("2026-10-01", "2000000"))
        self.assertEqual(st["waktu_terakhir"], "2026-10-01T10:00:00+07:00")
        self.assertNotIn("2026-09-30", st["buku_rugi_harian"])
        # jam kembali ke 1/10 14.00: rugi total Rp155.022 > Rp100.000 -> WAJIB berhenti
        kode, out = self.tick_pada("846667335", "2026-10-01T14:00:00+07:00")
        self.assertEqual(kode, 3, out)
        self.assertIn("BATAS RUGI HARIAN: turun Rp155.022", out)
        self.assertTrue(self.state()["berhenti"])

    def test_hari_efektif_tidak_pernah_mundur(self):
        c = cfg_dari()
        st = inti.state_awal(c)
        self.assertEqual(inti.hari_efektif(st, T0), ("2026-09-29", False))
        self.assertEqual(inti.hari_efektif(st, T0 - timedelta(days=3)), ("2026-09-29", True))
        self.assertEqual(inti.hari_efektif(st, T0 - timedelta(seconds=30)), ("2026-09-29", False))  # toleransi NTP
        self.assertEqual(inti.hari_efektif(st, T0 + timedelta(days=1)), ("2026-09-30", False))
        self.assertEqual(st["waktu_terakhir"], (T0 + timedelta(days=1)).isoformat())

    def test_state_lama_tanpa_waktu_terakhir(self):
        c = cfg_dari(batas_risiko=dict(DASAR["batas_risiko"], stop_loss_persen="90"))
        st = inti.state_awal(c)
        st.update(posisi_koin="10", biaya_perolehan="1000000", kas="0", hari="2026-09-29",
                  ekuitas_awal_hari="1000000", waktu_terakhir=None, buku_rugi_harian={})
        alasan, _ = inti.cek_risiko_awal(c, st, D("79999"), T0 - timedelta(days=1))   # jam mundur 1 hari
        self.assertIn("RUGI HARIAN", alasan)
        self.assertEqual(st["hari"], "2026-09-29")

    def test_lanjutkan_tidak_mereset_pengaman_jam(self):
        self.tulis_cfg(CFG_H1)
        lalu = (datetime.now(WIB) - timedelta(minutes=30)).replace(microsecond=0)
        self.tick_pada("1000000000", lalu.isoformat())
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp])
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        st = self.state()
        self.assertEqual(st["waktu_terakhir"], lalu.isoformat())
        self.assertEqual(st["buku_rugi_harian"], {})

    def test_lanjutkan_memperbaiki_waktu_masa_depan(self):
        self.tulis_cfg(CFG_H1)
        self.tick_pada("1000000000", "2099-01-01T08:00:00+07:00")   # jam pernah lompat jauh ke depan
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp])
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        self.assertIn("lebih maju dari jam komputer", out)
        self.assertLess(self.state()["waktu_terakhir"], "2099")


class M1Redirect(Folder):
    """M1: kunci API tidak boleh ikut terkirim ke host lain lewat redirect."""

    @classmethod
    def setUpClass(cls):
        cls.url, cls.k, cls.srv = mock_bursa.jalankan()
        cls.url2, cls.k2, cls.srv2 = mock_bursa.jalankan()
        cls.url2 = cls.url2.replace("127.0.0.1", "localhost")   # host berbeda

    @classmethod
    def tearDownClass(cls):
        for srv in (cls.srv, cls.srv2):
            srv.shutdown(); srv.server_close()

    def setUp(self):
        super().setUp()
        for k in (self.k, self.k2):
            k.permintaan.clear(); k.order.clear(); k.alihkan_ke = None

    def test_binance_bertanda_tidak_mengikuti_redirect(self):
        cfg = inti.normalisasi_konfigurasi({
            "mode": "testnet", "bursa": "binance", "pasangan": "BTCUSDT", "koin": "BTC", "kutipan": "USDT",
            "strategi": {"jenis": "dca", "nominal_per_beli": "100", "interval_jam": 24},
            "batas_risiko": {"modal_maks_per_order": "100", "modal_maks_total": "1000", "stop_loss_persen": "20",
                             "rugi_harian_maks": "100", "order_terbuka_maks": 2}, "kunci": {"env": True}})
        ad = bursa.Binance(cfg, "testnet", bursa.Kunci(mock_bursa.BINANCE_KEY, mock_bursa.BINANCE_SECRET, "uji"), self.url)
        self.k.alihkan_ke = self.url2
        with self.assertRaises(bursa.ErrorBursa) as cm:
            ad.jumlah_order_terbuka()
        self.assertIn("TIDAK dikirim ke alamat lain", str(cm.exception))
        with self.assertRaises(bursa.StatusTidakPasti):
            ad.order_pasar("beli", nilai_kutipan=D("100"))
        self.assertEqual(self.k2.permintaan, [])            # host tujuan tidak pernah menerima apa pun
        for r in self.k.permintaan:
            self.assertNotIn(mock_bursa.BINANCE_SECRET, r[3] + r[4])

    def test_indodax_tapi_redirect_ditolak_via_bot(self):
        c = copy.deepcopy(DASAR)
        p = os.path.join(self.tmp, "kunci.json")
        with open(p, "w") as f:
            json.dump({"api_key": mock_bursa.INDODAX_KEY, "api_secret": mock_bursa.INDODAX_SECRET}, f)
        os.chmod(p, 0o600)
        c.update(mode="testnet", kunci={"file": p})
        self.tulis_cfg(c)
        self.k.alihkan_ke = self.url2
        kode, out = self.tick("--url-uji", self.url)
        self.assertIn("mengalihkan", out)
        self.assertEqual(self.k2.permintaan, [])
        self.assertEqual(self.k.order, [])

    def test_publik_redirect_host_lain_ditolak(self):
        self.k.alihkan_ke = self.url2
        with self.assertRaises(bursa.ErrorBursa) as cm:
            bursa._http("GET", self.url + "/api/v3/time")
        self.assertIn("host lain tidak diikuti", str(cm.exception))
        self.assertEqual(self.k2.permintaan, [])


class M2PajakSwap(unittest.TestCase):
    """M2: PMK 50/2025 Pasal 11 ayat (2) huruf b & Pasal 12 ayat (5) huruf b -- swap kripto-kripto."""

    def cfg_usdt(self, pajak, fee="0"):
        return inti.normalisasi_konfigurasi({
            "mode": "paper", "bursa": "binance", "pasangan": "BTCUSDT", "koin": "BTC", "kutipan": "USDT",
            "strategi": {"jenis": "dca", "nominal_per_beli": "1000", "interval_jam": 24},
            "batas_risiko": {"modal_maks_per_order": "1000000000", "modal_maks_total": "1000000000",
                             "stop_loss_persen": "20", "rugi_harian_maks": "100", "order_terbuka_maks": 2},
            "biaya": {"fee_persen": fee, "pajak": pajak}})

    def test_contoh_resmi_lampiran_b(self):
        # Lampiran huruf B PMK 50/2025: 0,21% x (0,3 x Rp500.000.000) = Rp315.000 untuk MASING-MASING pihak.
        c = self.cfg_usdt("domestik")
        self.assertEqual(c["_d"]["tarif_pph_beli"], D("0.0021"))
        beli = inti.simulasi_isi(c, "beli", D("500000000"), D("150315000"))
        self.assertEqual((beli["jumlah"], beli["bruto"], beli["pajak"], beli["bersih"]),
                         (D("0.3"), D("150000000"), D("315000"), D("150315000")))
        jual = inti.simulasi_isi(c, "jual", D("500000000"), jumlah_koin=D("0.3"))
        self.assertEqual(jual["pajak"], D("315000"))

    def test_luar_negeri_1_persen_dua_sisi(self):
        c = self.cfg_usdt("luar_negeri", fee="0.1")
        beli = inti.simulasi_isi(c, "beli", D("60000"), D("100"))
        self.assertLessEqual(beli["bersih"], D("100"))
        self.assertEqual(beli["pajak"], (beli["bruto"] * D("0.01")).quantize(D("0.00000001"), rounding="ROUND_DOWN"))
        self.assertGreater(beli["pajak"], 0)
        self.assertEqual(beli["bersih"], beli["bruto"] + beli["fee"] + beli["pajak"])

    def test_pasangan_rupiah_beli_tanpa_pph(self):
        c = cfg_dari()
        self.assertEqual(c["_d"]["tarif_pph_beli"], D("0"))
        self.assertEqual(inti.simulasi_isi(c, "beli", D("1500000000"), D("100000"))["pajak"], D("0"))

    def test_rekap_menjumlahkan_pph_sisi_beli(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=jalankan_bot.KOLOM_TRANSAKSI)
            w.writeheader()
            w.writerow({"waktu": "2026-09-01T08:00:00+07:00", "pasangan": "BTCUSDT", "sisi": "beli",
                        "bruto": "99", "fee": "0", "pajak_pph": "0.99"})
            w.writerow({"waktu": "2026-09-02T08:00:00+07:00", "pasangan": "BTCUSDT", "sisi": "jual",
                        "bruto": "110", "fee": "0.11", "pajak_pph": "1.1"})
        kode, out = jalankan(hitung_pajak_biaya.main, ["--transaksi", f.name, "--kurs-idr", "16000"])
        os.remove(f.name)
        j = json.loads(out)["per_bulan"]["2026-09"]
        self.assertEqual((j["pph_idr"], j["pph_sisi_beli_idr"]), (33440, 15840))   # (0,99+1,1) x 16.000


class M3TombolBerhentiGlobal(Folder):
    """M3: tombol berhenti dihormati apa pun --folder-bot yang dipakai jadwal."""

    def test_folder_bot_berbeda_tetap_berhenti(self):
        self.tulis_cfg(DASAR)
        lain = os.path.join(self.tmp, "folder-lain")
        kode, out = self.tick("--folder-bot", lain, "--harga", "1500000000", "--sekarang", T0.isoformat())
        self.assertIn("BELI", out)
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp])     # tanpa --folder-bot
        self.assertIn(inti.folder_stop_global(), out)
        kode, out = self.tick("--folder-bot", lain, "--harga", "1500000000",
                              "--sekarang", (T0 + timedelta(days=2)).isoformat())
        self.assertEqual(kode, 3, out); self.assertIn("Tombol berhenti", out); self.assertNotIn("BELI", out)

    def test_hanya_file_global_tetap_berhenti(self):
        self.tulis_cfg(DASAR)
        lain = os.path.join(self.tmp, "folder-lain")
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp])
        os.remove(os.path.join(self.bot, "STOP"))            # file lokal terhapus/terlewat
        kode, out = self.tick("--folder-bot", lain, "--harga", "1500000000", "--sekarang", T0.isoformat())
        self.assertEqual(kode, 3, out); self.assertIn("STOP-", out)

    def test_stop_semua(self):
        self.tulis_cfg(DASAR)
        kode, out = jalankan(berhenti.main, ["--semua"])
        self.assertEqual(kode, 0)
        kode, out = self.tick("--harga", "1500000000", "--sekarang", T0.isoformat())
        self.assertEqual(kode, 3); self.assertIn("STOP-SEMUA", out)
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        self.assertEqual(kode, 1); self.assertIn("--cabut-semua", out)
        self.assertEqual(jalankan(berhenti.main, ["--cabut-semua"])[0], 1)     # wajib --saya-sudah-cek
        self.assertEqual(jalankan(berhenti.main, ["--cabut-semua", "--saya-sudah-cek"])[0], 0)
        self.assertEqual(jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])[0], 0)
        kode, out = self.tick("--harga", "1500000000", "--sekarang", (T0 + timedelta(days=1)).isoformat())
        self.assertIn("BELI", out)

    def test_lanjutkan_menghapus_semua_stop_bot_ini(self):
        self.tulis_cfg(DASAR)
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp])
        jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--lanjutkan", "--saya-sudah-cek"])
        self.assertEqual(inti.cek_tombol_berhenti(self.cfgp, self.bot), [])


class M4WithdrawIndodax(AlurMock):
    """M4: tanpa pemanggilan metode withdraw; daftar periksa manual wajib untuk live."""

    def cfg_indodax(self, mode):
        c = copy.deepcopy(DASAR)
        c.update(mode=mode)
        if mode != "paper":
            c["kunci"] = {"file": self.tulis_kunci(mock_bursa.INDODAX_KEY, mock_bursa.INDODAX_SECRET)}
        return c

    def test_live_indodax_wajib_daftar_periksa(self):
        self.tulis_cfg(self.cfg_indodax("paper"))
        self.tick("--url-uji", self.url)
        self.tulis_cfg(self.cfg_indodax("live"))
        self.suntik_bukti_paper()
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp])
        self.assertEqual(kode, 0, out)
        self.assertIn("DAFTAR PERIKSA WAJIB", out); self.assertIn("withdraw", out)
        frasa = f"LIVE {inti.sidik_jari_penuh(inti.muat_konfigurasi(self.cfgp))} SAYA TANGGUNG RISIKONYA"
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--frasa", frasa])
        self.assertEqual(kode, 2); self.assertIn("--saya-sudah-cek-tanpa-withdraw", out)
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):   # flag lama ditolak
            jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--frasa", frasa, "--kunci-tanpa-withdraw"])
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--cek-kunci", "--url-uji", self.url])
        self.assertEqual(kode, 0, out); self.assertIn("TIDAK diperiksa otomatis", out)
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--frasa", frasa,
                                                 "--saya-sudah-cek-tanpa-withdraw"])
        self.assertEqual(kode, 0, out)
        with open(os.path.join(self.bot, "KONFIRMASI-LIVE.json")) as f:
            k = json.load(f)
        self.assertTrue(k["daftar_periksa_withdraw_selesai"]); self.assertFalse(k["cek_izin_otomatis"])
        kode, out = self.tick("--url-uji", self.url, "--izinkan-live")
        self.assertEqual(kode, 2, out); self.assertIn("[LIVE", out)
        metode = [dict(__import__("urllib.parse").parse.parse_qsl(r[4])).get("method") for r in self.k.permintaan
                  if r[1] == "/tapi"]
        self.assertTrue(metode)
        self.assertFalse([m for m in metode if m and "withdraw" in m.lower()])

    def test_konfirmasi_lama_tanpa_daftar_periksa_ditolak(self):
        self.tulis_cfg(self.cfg_indodax("paper"))
        self.tick("--url-uji", self.url)
        self.tulis_cfg(self.cfg_indodax("live"))
        self.suntik_bukti_paper()
        kode_k = inti.sidik_jari_penuh(inti.muat_konfigurasi(self.cfgp))
        with open(os.path.join(self.bot, "KONFIRMASI-LIVE.json"), "w") as f:   # format 1.0.0
            json.dump({"kode": kode_k, "frasa": f"LIVE {kode_k} SAYA TANGGUNG RISIKONYA",
                       "pernyataan_kunci_tanpa_withdraw": True}, f)
        kode, out = self.tick("--url-uji", self.url, "--izinkan-live")
        self.assertEqual(kode, 3); self.assertIn("daftar periksa", out)
        self.assertEqual(self.k.order, [])

    def test_kode_sumber_tanpa_metode_withdraw(self):
        import re
        for n in os.listdir(os.path.join(SKILL, "scripts")):
            if n.endswith(".py"):
                with open(os.path.join(SKILL, "scripts", n), encoding="utf-8") as f:
                    kode = "\n".join(b for b in f.read().splitlines() if not b.strip().startswith("#"))
                self.assertIsNone(re.search(r"_tapi\(\s*[\"'](withdraw|transfer)", kode, re.I), n)
                self.assertIsNone(re.search(r"[\"']/(sapi/v1/capital/withdraw|wapi)", kode), n)


class LowRevisi(AlurMock):
    """L1-L7 dari HASIL-UJI 1.0.0."""

    def test_l1_pemisah_ribuan_ditolak(self):
        for nilai in ("500.000", "1.500.000", "2,500"):
            with self.assertRaises(inti.KonfigurasiTidakValid) as cm:
                cfg_dari(batas_risiko=dict(DASAR["batas_risiko"], modal_maks_total=nilai))
            self.assertIn("pemisah ribuan", str(cm.exception))
        self.assertEqual(inti.angka("0.001", "x"), D("0.001"))
        self.assertEqual(inti.angka("1.25", "x"), D("1.25"))

    def test_l2_nilai_ekstrem_ditolak_tanpa_traceback(self):
        for st in ({"jenis": "dca", "nominal_per_beli": "100000", "interval_jam": "1e20"},
                   {"jenis": "dca", "nominal_per_beli": "100000", "interval_jam": "100000000"}):
            with self.assertRaises(inti.KonfigurasiTidakValid):
                cfg_dari(strategi=st)
        with self.assertRaises(inti.KonfigurasiTidakValid):
            cfg_dari(batas_risiko=dict(DASAR["batas_risiko"], modal_maks_total="1e30"))
        asli = jalankan_bot.satu_putaran
        jalankan_bot.satu_putaran = lambda a: (_ for _ in ()).throw(OverflowError("uji"))
        try:
            self.tulis_cfg(DASAR)
            kode, out = self.tick("--openclaw")
        finally:
            jalankan_bot.satu_putaran = asli
        self.assertEqual(kode, 0); self.assertIn("kesalahan tak terduga", out); self.assertNotIn("Traceback", out)
        kode, out = jalankan(siapkan_live.main, ["--konfigurasi", self.cfgp, "--cek-kunci", "--url-uji", "https://x.example"])
        self.assertNotIn("Traceback", out)

    def test_l3_harga_nol_tanpa_order(self):
        self.tulis_cfg(self.cfg_binance("testnet"))
        self.k.harga_btcusdt = D("0")
        kode, out = self.tick("--url-uji", self.url)
        self.assertIn("tidak wajar", out)
        self.assertEqual([r for r in self.k.permintaan if r[0] == "POST"], [])
        with self.assertRaises(ValueError):
            inti.simulasi_isi(cfg_dari(), "beli", D("0"), D("100000"))

    def test_l4_live_butuh_paper_harga_asli_24_jam(self):
        c = self.cfg_binance("paper")
        self.tulis_cfg(c)
        for _ in range(5):
            self.tick("--url-uji", self.url)          # server tiruan tidak dihitung sebagai harga asli
        self.tulis_cfg(dict(c, mode="live", saya_paham_binance_bukan_pakd_ojk=True))
        self.suntik_bukti_paper(jam=10, putaran=5)    # 5 putaran tapi hanya 10 jam
        kode, out = self.tick("--url-uji", self.url, "--izinkan-live")
        self.assertEqual(kode, 3); self.assertIn("bukti simulasi belum cukup", out)

    def test_l5_kunci_putaran_atomik(self):
        p = os.path.join(self.tmp, ".sedang-jalan")
        self.assertTrue(jalankan_bot.ambil_kunci_putaran(p, "a"))
        self.assertFalse(jalankan_bot.ambil_kunci_putaran(p, "b"))
        lama = datetime.now().timestamp() - 700
        os.utime(p, (lama, lama))
        self.assertTrue(jalankan_bot.ambil_kunci_putaran(p, "c"))     # kunci basi diambil alih

    def test_l6_batalkan_order_sinkron_waktu(self):
        self.tulis_cfg(self.cfg_binance("testnet"))
        self.k.order_terbuka = 1
        kode, out = jalankan(berhenti.main, ["--konfigurasi", self.cfgp, "--batalkan-order", "--url-uji", self.url])
        self.assertIn("dibatalkan: 1", out)
        jalur = [r[1] for r in self.k.permintaan]
        self.assertLess(jalur.index("/api/v3/time"), jalur.index("/api/v3/openOrders"))

    def test_l7_catatan_grid(self):
        c = copy.deepcopy(DASAR)
        c["strategi"] = {"jenis": "grid", "harga_bawah": "100", "harga_atas": "200", "jumlah_grid": 4,
                         "nominal_per_grid": "100000"}
        self.tulis_cfg(c)
        self.tick("--harga", "130", "--sekarang", T0.isoformat())
        kode, out = self.tick("--harga", "150", "--sekarang", (T0 + timedelta(hours=1)).isoformat())
        self.assertIn("harga rata-rata SEMUA koin", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
