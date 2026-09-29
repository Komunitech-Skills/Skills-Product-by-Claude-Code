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

    def setUp(self):
        super().setUp()
        k = self.k
        k.withdraw_aktif, k.order_terbuka, k.putus_saat_order, k.tolak_order = False, 0, False, None
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


if __name__ == "__main__":
    unittest.main(verbosity=1)
