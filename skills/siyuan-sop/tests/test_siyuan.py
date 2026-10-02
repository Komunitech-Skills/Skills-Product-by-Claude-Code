#!/usr/bin/env python3
"""Uji unit untuk scripts/siyuan.py memakai server kernel SiYuan TIRUAN (http.server standar).

Server tiruan berjalan di 127.0.0.1 pada thread terpisah, TIDAK butuh SiYuan asli maupun internet.
Bentuk jawaban meniru /api/... resmi (lihat references/api-endpoints.md untuk sumber & tanggal
verifikasi). Jalankan:  python3 -m unittest discover -s tests   (Windows: python / py)
"""
import io
import json
import os
import stat
import sys
import tempfile
import threading
import unittest
import contextlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SINI, "..", "scripts"))
import siyuan  # noqa: E402

TOKEN_BENAR = "tokenujiSIYUAN0123456789abcdef"


class Keadaan:
    def __init__(self):
        self.reset()

    def reset(self):
        self.notebooks = [
            {"id": "20260101000000-aaaaaaa", "name": "Toko Hijab Cantik", "icon": "1f4d4", "sort": 0,
             "closed": False},
            {"id": "20260101000001-bbbbbbb", "name": "Arsip Lama", "icon": "1f4c1", "sort": 1, "closed": True},
        ]
        self.docs = {
            "20260201000000-doc0001": {"box": "20260101000000-aaaaaaa", "hpath": "/FAQ/Ongkos Kirim",
                                        "content": "Ongkir dihitung otomatis oleh kurir saat checkout.",
                                        "updated": "20260901120000"},
            "20260201000000-doc0002": {"box": "20260101000000-aaaaaaa", "hpath": "/SOP/Packing Pesanan",
                                        "content": "1. Cek pesanan. 2. Bungkus rapi. 3. Tempel label.",
                                        "updated": "20260601090000"},
        }
        self.hpath_index = {(d["box"], d["hpath"]): doc_id for doc_id, d in self.docs.items()}
        self.mode = set()  # 'unauthorized' | '5xx' | 'sebagian'
        self.log = []  # daftar (path, payload dict) yang diterima


K = Keadaan()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _baca_json(self):
        n = int(self.headers.get("Content-Length", 0))
        mentah = self.rfile.read(n) if n else b"{}"
        try:
            return json.loads(mentah.decode("utf-8"))
        except ValueError:
            return {}

    def _balas(self, obj, kode=200):
        badan = json.dumps(obj).encode("utf-8")
        if "sebagian" in K.mode:
            badan = badan[: max(1, len(badan) // 3)]
        self.send_response(kode)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(badan)))
        self.end_headers()
        self.wfile.write(badan)

    def do_POST(self):
        payload = self._baca_json()
        K.log.append((self.path, payload))
        auth = self.headers.get("Authorization", "")
        if "unauthorized" in K.mode:
            return self._balas({"code": -1, "msg": "Invalid Auth", "data": None}, 401)
        if auth != "Token " + TOKEN_BENAR:
            return self._balas({"code": -1, "msg": "Invalid Auth", "data": None}, 401)
        if "5xx" in K.mode:
            return self._balas({"code": -1, "msg": "internal error"}, 500)

        if self.path == "/api/notebook/lsNotebooks":
            return self._balas({"code": 0, "msg": "", "data": {"notebooks": K.notebooks}})
        if self.path == "/api/notebook/openNotebook":
            return self._balas({"code": 0, "msg": "", "data": None})
        if self.path == "/api/filetree/getIDsByHPath":
            key = (payload.get("notebook"), payload.get("path"))
            ids = [K.hpath_index[key]] if key in K.hpath_index else []
            return self._balas({"code": 0, "msg": "", "data": ids})
        if self.path == "/api/filetree/createDocWithMd":
            new_id = "20260301000000-" + str(len(K.docs) + 1).zfill(7)
            box, path, md = payload["notebook"], payload["path"], payload.get("markdown", "")
            K.docs[new_id] = {"box": box, "hpath": path, "content": md, "updated": "20260901000000"}
            K.hpath_index[(box, path)] = new_id
            return self._balas({"code": 0, "msg": "", "data": new_id})
        if self.path == "/api/filetree/removeDocByID":
            doc_id = payload["id"]
            d = K.docs.pop(doc_id, None)
            if d:
                K.hpath_index.pop((d["box"], d["hpath"]), None)
            return self._balas({"code": 0, "msg": "", "data": None})
        if self.path == "/api/block/appendBlock":
            parent = payload["parentID"]
            if parent in K.docs:
                K.docs[parent]["content"] += "\n" + payload["data"]
            return self._balas({"code": 0, "msg": "", "data": [{"doOperations": []}]})
        if self.path == "/api/export/exportMdContent":
            d = K.docs.get(payload.get("id"))
            if not d:
                return self._balas({"code": -1, "msg": "not found", "data": None})
            return self._balas({"code": 0, "msg": "", "data": {"hPath": d["hpath"], "content": d["content"]}})
        if self.path == "/api/query/sql":
            return self._balas({"code": 0, "msg": "", "data": self._sql(payload.get("stmt", ""))})
        return self._balas({"code": -1, "msg": "unknown endpoint " + self.path}, 404)

    def _sql(self, stmt):
        baris = [{"id": doc_id, "root_id": doc_id, "box": d["box"], "hpath": d["hpath"], "content": d["content"],
                  "type": "d", "updated": d["updated"]} for doc_id, d in K.docs.items()]
        if "updated < '" in stmt:
            cutoff = stmt.split("updated < '", 1)[1].split("'", 1)[0]
            hasil = [b for b in baris if b["updated"] < cutoff]
            if "box='" in stmt:
                box = stmt.split("box='", 1)[1].split("'", 1)[0]
                hasil = [b for b in hasil if b["box"] == box]
            return hasil
        if "LIKE '%" in stmt:
            # Ambil kata pertama di antara '%...%' pada klausa content LIKE untuk pencarian tiruan.
            bagian = stmt.split("content LIKE '%", 1)[1].split("%'", 1)[0]
            kata = bagian.replace("\\%", "%").replace("\\_", "_").replace("''", "'").lower()
            return [b for b in baris if kata in b["content"].lower() or kata in b["hpath"].lower()]
        if "box='" in stmt:
            box = stmt.split("box='", 1)[1].split("'", 1)[0]
            return [b for b in baris if b["box"] == box]
        return baris


class UjiSiyuan(unittest.TestCase):
    server = None
    thread = None
    url = None

    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=5)

    def setUp(self):
        K.reset()
        siyuan._RAHASIA.clear()
        self._tmp = tempfile.TemporaryDirectory()
        self._asli_default = siyuan.FILE_KUNCI_DEFAULT
        siyuan.FILE_KUNCI_DEFAULT = os.path.join(self._tmp.name, "tidak-ada", "kunci.txt")
        self._cwd = os.getcwd()
        os.chdir(self._tmp.name)

    def tearDown(self):
        os.chdir(self._cwd)
        siyuan.FILE_KUNCI_DEFAULT = self._asli_default
        self._tmp.cleanup()

    # -------- utilitas
    def jalan(self, argv, token=TOKEN_BENAR, izinkan=False):
        penuh = ["--url", self.url]
        if not izinkan:
            pass
        else:
            penuh.append("--izinkan-jarak-jauh")
        penuh += argv
        os.environ["SIYUAN_TOKEN"] = token or ""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = siyuan.main(penuh)
        return kode, out.getvalue()

    # -------- koneksi & token
    def test_01_cek_ok(self):
        kode, out = self.jalan(["cek"])
        self.assertEqual(kode, 0)
        self.assertIn("Toko Hijab Cantik", out)

    def test_02_token_salah_401(self):
        kode, out = self.jalan(["cek"], token="token-salah-sekali")
        self.assertEqual(kode, siyuan.KELUAR_AKSES)
        self.assertIn("Token API ditolak", out)

    def test_03_token_belum_diatur(self):
        os.environ.pop("SIYUAN_TOKEN", None)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = siyuan.main(["--url", self.url, "cek"])
        self.assertEqual(kode, siyuan.KELUAR_AKSES)
        self.assertIn("belum diatur", out.getvalue())

    def test_04_kernel_tidak_menyala(self):
        import socket
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        os.environ["SIYUAN_TOKEN"] = TOKEN_BENAR
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = siyuan.main(["--url", f"http://127.0.0.1:{port}", "cek"])
        self.assertEqual(kode, siyuan.KELUAR_KONEKSI)
        self.assertIn("Tidak bisa terhubung", out.getvalue())

    def test_05_tolak_non_localhost_tanpa_izin(self):
        os.environ["SIYUAN_TOKEN"] = TOKEN_BENAR
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = siyuan.main(["--url", "http://203.0.113.5:6806", "cek"])
        self.assertEqual(kode, siyuan.KELUAR_AKSES)
        self.assertIn("bukan komputer ini", out.getvalue())
        self.assertEqual(K.log, [])  # tidak ada permintaan yang benar-benar dikirim

    def test_06_non_localhost_wajib_https(self):
        os.environ["SIYUAN_TOKEN"] = TOKEN_BENAR
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = siyuan.main(["--url", "http://203.0.113.5:6806", "--izinkan-jarak-jauh", "cek"])
        self.assertEqual(kode, siyuan.KELUAR_AKSES)
        self.assertIn("wajib https", out.getvalue())

    def test_07_token_tidak_pernah_tercetak(self):
        kode, out = self.jalan(["cek"])
        self.assertNotIn(TOKEN_BENAR, out)

    def test_08_server_5xx_saat_baca(self):
        K.mode.add("5xx")
        kode, out = self.jalan(["cek"])
        self.assertEqual(kode, siyuan.KELUAR_TIDAK_PASTI)

    def test_09_kunci_file_menang_atas_env(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "kunci.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write(TOKEN_BENAR + "\n")
            os.environ["SIYUAN_TOKEN"] = "token-env-salah"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                kode = siyuan.main(["--url", self.url, "--kunci-file", p, "cek"])
            self.assertEqual(kode, 0)
            self.assertIn("PERINGATAN", out.getvalue())

    # -------- simpan-kunci
    def test_10_simpan_kunci_baru(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "sub", "kunci.txt")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                kode = siyuan.main(["--kunci-file", p, "simpan-kunci", "--token", "abc123"])
            self.assertEqual(kode, 0)
            with open(p, encoding="utf-8") as f:
                self.assertEqual(f.read().strip(), "abc123")
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(os.stat(p).st_mode), 0o600)

    def test_11_simpan_kunci_tolak_timpa_tanpa_ya(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "kunci.txt")
            with open(p, "w", encoding="utf-8") as f:
                f.write("lama\n")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                kode = siyuan.main(["--kunci-file", p, "simpan-kunci", "--token", "baru"])
            self.assertEqual(kode, siyuan.KELUAR_ARG)
            self.assertIn("sudah ada", out.getvalue())

    # -------- daftar-buku
    def test_12_daftar_buku(self):
        kode, out = self.jalan(["daftar-buku"])
        self.assertEqual(kode, 0)
        self.assertIn("Arsip Lama", out)
        self.assertIn("[tertutup]", out)

    # -------- cari
    def test_13_cari_ditemukan(self):
        kode, out = self.jalan(["cari", "ongkir"])
        self.assertEqual(kode, 0)
        self.assertIn("Ongkos Kirim", out)

    def test_14_cari_tidak_ditemukan(self):
        kode, out = self.jalan(["cari", "katatidakadasamasekali"])
        self.assertEqual(kode, 0)
        self.assertIn("Tidak ada dokumen", out)

    def test_15_cari_kosong_ditolak(self):
        kode, out = self.jalan(["cari", "  "])
        self.assertEqual(kode, siyuan.KELUAR_ARG)

    def test_16_cari_suntik_petik_tunggal(self):
        kode, out = self.jalan(["cari", "ongkir' OR '1'='1"])
        self.assertEqual(kode, 0)
        stmt = K.log[-1][1]["stmt"]
        self.assertNotIn("' OR '1'='1", stmt.replace("''", ""))  # sudah digandakan, bukan pemisah string
        self.assertIn("''", stmt)

    def test_17_cari_suntik_drop_table(self):
        kode, out = self.jalan(["cari", "x'; DROP TABLE blocks; --"])
        self.assertEqual(kode, 0)
        stmt = K.log[-1][1]["stmt"]
        self.assertIn("DROP TABLE blocks", stmt)  # tetap ada sebagai TEKS di dalam literal, bukan dieksekusi
        self.assertTrue(stmt.strip().upper().startswith("SELECT"))
        self.assertEqual(stmt.upper().count("SELECT"), 1)  # hanya satu pernyataan, tidak ada penumpukan statement

    def test_18_cari_emoji_unicode(self):
        K.docs["20260301000009-doc9"] = {"box": "20260101000000-aaaaaaa", "hpath": "/FAQ/Jam Buka 🕐",
                                          "content": "Buka jam 9 pagi 😊", "updated": "20260901000000"}
        kode, out = self.jalan(["cari", "😊"])
        self.assertEqual(kode, 0)
        self.assertIn("Jam Buka", out)

    # -------- baca
    def test_19_baca_by_id(self):
        kode, out = self.jalan(["baca", "--id", "20260201000000-doc0002"])
        self.assertEqual(kode, 0)
        self.assertIn("Packing Pesanan", out)
        self.assertIn("Bungkus rapi", out)

    def test_20_baca_by_path(self):
        kode, out = self.jalan(["baca", "--notebook", "20260101000000-aaaaaaa", "--path", "/FAQ/Ongkos Kirim"])
        self.assertEqual(kode, 0)
        self.assertIn("Ongkir dihitung otomatis", out)

    def test_21_baca_path_tidak_ada(self):
        kode, out = self.jalan(["baca", "--notebook", "20260101000000-aaaaaaa", "--path", "/tidak/ada"])
        self.assertNotEqual(kode, 0)

    def test_22_baca_argumen_kurang(self):
        kode, out = self.jalan(["baca"])
        self.assertEqual(kode, siyuan.KELUAR_ARG)

    # -------- buat
    def test_23_buat_pratinjau_tidak_menulis(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/SOP/Baru",
                                 "--md", "isi baru"])
        self.assertEqual(kode, 0)
        self.assertIn("PRATINJAU", out)
        self.assertNotIn(("20260101000000-aaaaaaa", "/SOP/Baru"), K.hpath_index)

    def test_24_buat_dengan_ya_tersimpan(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/SOP/Baru",
                                 "--md", "isi baru", "--ya"])
        self.assertEqual(kode, 0)
        self.assertIn("TERSIMPAN", out)
        self.assertIn(("20260101000000-aaaaaaa", "/SOP/Baru"), K.hpath_index)

    def test_25_buat_tolak_timpa_tanpa_flag(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/FAQ/Ongkos Kirim",
                                 "--md", "isi ganti", "--ya"])
        self.assertEqual(kode, siyuan.KELUAR_DOBEL)
        self.assertIn("sudah ada dokumen", out)
        self.assertEqual(K.docs["20260201000000-doc0001"]["content"], "Ongkir dihitung otomatis oleh kurir saat checkout.")

    def test_26_buat_timpa_tanpa_ya_tidak_menghapus(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/FAQ/Ongkos Kirim",
                                 "--md", "isi ganti", "--timpa"])
        self.assertEqual(kode, 0)
        self.assertIn("PRATINJAU", out)
        self.assertIn("20260201000000-doc0001", K.docs)  # dokumen lama belum terhapus

    def test_27_buat_timpa_dengan_ya_mengganti(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/FAQ/Ongkos Kirim",
                                 "--md", "isi ganti total", "--timpa", "--ya", "--konfirmasi-timpa"])
        self.assertEqual(kode, 0)
        self.assertNotIn("20260201000000-doc0001", K.docs)
        baru = K.hpath_index[("20260101000000-aaaaaaa", "/FAQ/Ongkos Kirim")]
        self.assertEqual(K.docs[baru]["content"], "isi ganti total")

    def test_27b_timpa_ya_tanpa_konfirmasi_ditolak(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/FAQ/Ongkos Kirim",
                                 "--md", "isi ganti", "--timpa", "--ya"])
        self.assertEqual(kode, siyuan.KELUAR_ARG)
        self.assertIn("konfirmasi", out)
        self.assertIn("20260201000000-doc0001", K.docs)
        self.assertFalse(os.path.exists("cadangan-siyuan"))

    def test_27c_pratinjau_timpa_menampilkan_isi_lama_dan_judul(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/SOP/Packing Pesanan",
                                 "--md", "baru", "--timpa"])
        self.assertEqual(kode, 0)
        self.assertIn("Packing Pesanan", out)
        self.assertIn("ISI LAMA", out)
        self.assertIn("Bungkus rapi", out)
        self.assertIn("konfirmasi akhir", out)
        self.assertIn("20260201000000-doc0002", K.docs)

    def test_27d_timpa_membuat_cadangan_isi_lama(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/SOP/Packing Pesanan",
                                 "--md", "baru", "--timpa", "--ya", "--konfirmasi-timpa"])
        self.assertEqual(kode, 0)
        self.assertIn("Cadangan", out)
        berkas = os.listdir("cadangan-siyuan")
        self.assertEqual(len(berkas), 1)
        self.assertIn("-sebelum-", berkas[0])
        with open(os.path.join("cadangan-siyuan", berkas[0]), encoding="utf-8") as f:
            isi = f.read()
        self.assertIn("Bungkus rapi", isi)
        self.assertNotIn("baru", isi.replace("Bungkus", ""))

    def test_27e_cari_menyertakan_id_dan_petunjuk_baca(self):
        kode, out = self.jalan(["cari", "ongkir"])
        self.assertEqual(kode, 0)
        self.assertIn("id 20260201000000-doc0001", out)
        self.assertIn("baca --id", out)

    def test_09b_kunci_tersimpan_menang_atas_env_default(self):
        p = siyuan.FILE_KUNCI_DEFAULT
        os.makedirs(os.path.dirname(p))
        with open(p, "w", encoding="utf-8") as f:
            f.write(TOKEN_BENAR + "\n")
        os.chmod(p, 0o600)
        kode, out = self.jalan(["cek"], token="token-tempelan-chat-salah")
        self.assertEqual(kode, 0)
        self.assertIn("PERINGATAN", out)
        self.assertIn("DIABAIKAN", out)
        self.assertNotIn("token-tempelan-chat-salah", out)

    def test_09c_simpan_kunci_dengan_argumen_token_memberi_peringatan(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = siyuan.main(["--url", self.url, "simpan-kunci", "--token", TOKEN_BENAR])
        self.assertEqual(kode, 0)
        self.assertIn("PERINGATAN", out.getvalue())

    def test_28_buat_path_wajib_garis_miring(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "SOP/Baru",
                                 "--md", "x"])
        self.assertEqual(kode, siyuan.KELUAR_ARG)

    def test_29_buat_tanpa_isi_markdown(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/SOP/Kosong"])
        self.assertEqual(kode, siyuan.KELUAR_ARG)

    def test_30_buat_judul_emoji_unicode(self):
        kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/FAQ/Jam Buka 🕐",
                                 "--md", "Buka 09.00 - 21.00 setiap hari 😊", "--ya"])
        self.assertEqual(kode, 0)
        doc_id = K.hpath_index[("20260101000000-aaaaaaa", "/FAQ/Jam Buka 🕐")]
        self.assertIn("😊", K.docs[doc_id]["content"])

    def test_31_buat_dari_stdin(self):
        stdin_lama = sys.stdin
        sys.stdin = io.StringIO("isi dari stdin")
        try:
            kode, out = self.jalan(["buat", "--notebook", "20260101000000-aaaaaaa", "--path", "/SOP/DariStdin",
                                     "--stdin", "--ya"])
        finally:
            sys.stdin = stdin_lama
        self.assertEqual(kode, 0)
        doc_id = K.hpath_index[("20260101000000-aaaaaaa", "/SOP/DariStdin")]
        self.assertEqual(K.docs[doc_id]["content"], "isi dari stdin")

    # -------- tambah
    def test_32_tambah_pratinjau_tidak_menulis(self):
        isi_lama = K.docs["20260201000000-doc0002"]["content"]
        kode, out = self.jalan(["tambah", "--id", "20260201000000-doc0002", "--md", "baris tambahan"])
        self.assertEqual(kode, 0)
        self.assertIn("PRATINJAU", out)
        self.assertEqual(K.docs["20260201000000-doc0002"]["content"], isi_lama)

    def test_33_tambah_dengan_ya(self):
        kode, out = self.jalan(["tambah", "--id", "20260201000000-doc0002", "--md", "baris tambahan", "--ya"])
        self.assertEqual(kode, 0)
        self.assertIn("baris tambahan", K.docs["20260201000000-doc0002"]["content"])

    def test_34_tambah_tanpa_id(self):
        ap_error = False
        try:
            self.jalan(["tambah", "--md", "x", "--ya"])
        except SystemExit:
            ap_error = True
        self.assertTrue(ap_error)  # argparse: --id wajib diisi

    # -------- lama
    def test_35_lama_default(self):
        kode, out = self.jalan(["lama"])
        self.assertEqual(kode, 0)
        self.assertIn("Packing Pesanan", out)  # 90+ hari sejak Juni

    def test_36_lama_hari_invalid(self):
        kode, out = self.jalan(["lama", "--hari", "0"])
        self.assertEqual(kode, siyuan.KELUAR_ARG)

    def test_37_lama_dengan_notebook_filter(self):
        kode, out = self.jalan(["lama", "--hari", "30", "--notebook", "20260101000000-aaaaaaa"])
        self.assertEqual(kode, 0)

    # -------- ekspor-basis
    def test_38_ekspor_basis(self):
        with tempfile.TemporaryDirectory() as d:
            tujuan = os.path.join(d, "gabungan.md")
            kode, out = self.jalan(["ekspor-basis", "--notebook", "20260101000000-aaaaaaa", "--file", tujuan])
            self.assertEqual(kode, 0)
            with open(tujuan, encoding="utf-8") as f:
                isi = f.read()
            self.assertIn("Ongkos Kirim", isi)
            self.assertIn("Packing Pesanan", isi)

    def test_39_ekspor_basis_filter(self):
        with tempfile.TemporaryDirectory() as d:
            tujuan = os.path.join(d, "gabungan.md")
            kode, out = self.jalan(["ekspor-basis", "--notebook", "20260101000000-aaaaaaa", "--file", tujuan,
                                     "--filter", "FAQ"])
            self.assertEqual(kode, 0)
            with open(tujuan, encoding="utf-8") as f:
                isi = f.read()
            self.assertIn("Ongkos Kirim", isi)
            self.assertNotIn("Packing Pesanan", isi)

    def test_40_ekspor_basis_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            tujuan = os.path.join(d, "g.md")
            kode, out = self.jalan(["ekspor-basis", "--notebook", "buku-tidak-ada", "--file", tujuan])
            self.assertEqual(kode, 0)
            self.assertIn("Tidak ada dokumen", out)

    # -------- mode --json
    def test_42_ekspor_basis_lewati_dokumen_induk_kosong(self):
        K.docs["20260301000000-induk"] = {
            "box": "20260101000000-aaaaaaa", "hpath": "/FAQ",
            "content": "---\ntitle: FAQ\ndate: 2026-09-26T09:42:09Z\nlastmod: 2026-09-26T09:42:09Z\n---\n\n# FAQ\n\n‍",
            "updated": "20260901000000",
        }
        with tempfile.TemporaryDirectory() as d:
            tujuan = os.path.join(d, "g.md")
            kode, out = self.jalan(["ekspor-basis", "--notebook", "20260101000000-aaaaaaa", "--file", tujuan])
            self.assertEqual(kode, 0)
            with open(tujuan, encoding="utf-8") as f:
                isi = f.read()
            self.assertNotIn("# /FAQ\n", isi)
            self.assertIn("Ongkos Kirim", isi)

    def test_41_json_output(self):
        kode, out = self.jalan(["--json", "daftar-buku"])
        self.assertEqual(kode, 0)
        data = json.loads(out)
        self.assertEqual(len(data["buku_catatan"]), 2)



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "siyuan.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["--kunci-file", os.path.join(t, "k.txt"), "simpan-kunci", "--token", "x", "--y"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "k.txt")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main()
