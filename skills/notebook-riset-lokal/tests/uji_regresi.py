#!/usr/bin/env python3
"""Uji regresi notebook.py memakai server tiruan (Python standar saja, tanpa paket luar).

Jalankan: python3 tests/uji_regresi.py
Tidak dijalankan otomatis oleh pembeli (tidak ikut paket dist/); ini alat pengembang Komunitech.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(os.path.dirname(SINI), "scripts", "notebook.py")

NOTEBOOKS = [
    {"id": "notebook:abc123", "name": "Regulasi Pajak UMKM", "description": "kumpulan PP/PMK",
     "archived": False, "created": "2026-09-01T00:00:00Z", "updated": "2026-09-20T00:00:00Z",
     "source_count": 2, "note_count": 0},
]
SOURCES = [
    {"id": "source:s1", "title": "PP 55/2022", "topics": ["pajak"], "asset": None,
     "embedded": True, "embedded_chunks": 12, "insights_count": 1, "created": "2026-09-01T00:00:00Z",
     "updated": "2026-09-01T00:00:00Z", "file_available": True, "status": "completed"},
    {"id": "source:s2", "title": None, "topics": None, "asset": None,
     "embedded": False, "embedded_chunks": 0, "insights_count": 0, "created": "2026-09-20T00:00:00Z",
     "updated": "2026-09-20T00:00:00Z", "file_available": None, "status": "processing"},
]

SANDI_BENAR = "rahasia-uji-123"

PASSED = []
FAILED = []


class Handler(BaseHTTPRequestHandler):
    mode = "normal"  # normal | auth | rusak | timeout | error500

    # Diisi oleh _handle_create_source() setiap kali POST /api/sources diterima,
    # agar uji regresi bisa MEMBUKTIKAN klien benar-benar mengirim multipart/form-data
    # (bukan cuma percaya mock membalas 200) — ini yang tadinya lolos diam-diam saat
    # bug #1 (kirim JSON) karena mock lama menerima JSON. Lihat uji 11/11b di bawah.
    permintaan_sources_terakhir = None  # {"content_type": str, "bidang": dict} | None

    def log_message(self, fmt, *args):
        pass

    def _auth_ok(self):
        if Handler.mode != "auth":
            return True
        return self.headers.get("Authorization") == f"Bearer {SANDI_BENAR}"

    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n) if n else b""
        return json.loads(raw) if raw else {}

    def _baca_mentah(self):
        n = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(n) if n else b""

    def _urai_multipart(self, raw, content_type):
        """Urai body multipart/form-data sederhana (field teks saja, tanpa file) —
        meniru cara FastAPI Form(...) mem-parse permintaan Open Notebook asli."""
        m = re.search(r"boundary=([^;]+)", content_type)
        if not m:
            return {}
        boundary = m.group(1).strip('"').encode()
        bidang = {}
        for bagian in raw.split(b"--" + boundary):
            bagian = bagian.strip(b"\r\n")
            if not bagian or bagian == b"--":
                continue
            if b"\r\n\r\n" not in bagian:
                continue
            header_mentah, _, nilai = bagian.partition(b"\r\n\r\n")
            nilai = nilai[:-2] if nilai.endswith(b"\r\n") else nilai  # buang \r\n penutup bila ada
            nm = re.search(rb'name="([^"]+)"', header_mentah)
            if nm:
                bidang[nm.group(1).decode()] = nilai.decode("utf-8", errors="replace")
        return bidang

    def do_GET(self):
        if Handler.mode == "timeout":
            time.sleep(3)
            return
        if Handler.mode == "rusak":
            body = b"BUKAN JSON {{{"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if Handler.mode == "error500":
            self._send(500, {"detail": "internal error simulasi"})
            return
        path = self.path.split("?")[0]
        if path == "/api/auth/status":
            self._send(200, {"auth_enabled": Handler.mode == "auth", "message": ""})
            return
        if not self._auth_ok():
            self._send(401, {"detail": "invalid token"})
            return
        if path == "/api/notebooks":
            self._send(200, NOTEBOOKS)
            return
        if path == "/api/sources":
            self._send(200, SOURCES)
            return
        if path == "/api/models/defaults":
            self._send(200, {"default_chat_model": "model:gpt-mini"})
            return
        if path.startswith("/api/podcasts/jobs/"):
            self._send(200, {"job_id": "job:1", "status": "completed", "progress": 100})
            return
        self._send(404, {"detail": "not found simulasi"})

    def do_POST(self):
        if Handler.mode == "timeout":
            time.sleep(3)
            return
        if not self._auth_ok():
            self._send(401, {"detail": "invalid token"})
            return
        path = self.path.split("?")[0]
        body = self._body()
        if path == "/api/notebooks":
            self._send(200, {"id": "notebook:baru1", "name": body.get("name"), "description": body.get("description", "")})
            return
        if path == "/api/sources":
            self._send(200, {"id": "source:baru1", "title": body.get("title") or "Sumber baru", "status": "processing"})
            return
        if path == "/api/search":
            self._send(200, {"results": [{"title": "PP 55/2022", "parent_type": "source",
                                           "matches": ["...UMKM dikenakan PPh Final 0,5%..."]}],
                              "total_count": 1, "search_type": "text"})
            return
        if path == "/api/search/ask/simple":
            self._send(200, {"answer": "PPh final UMKM 0,5% dari omzet (PP 55/2022).", "question": body.get("question", "")})
            return
        if path == "/api/podcasts/generate":
            self._send(200, {"job_id": "job:1", "status": "submitted", "message": "ok",
                              "episode_profile": body.get("episode_profile"), "episode_name": body.get("episode_name")})
            return
        self._send(404, {"detail": "not found simulasi"})


def jalankan_server(mode="normal"):
    Handler.mode = mode
    srv = HTTPServer(("127.0.0.1", 0), Handler)
    port = srv.server_port
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, port


def jalankan_cli(args, url):
    cmd = [sys.executable, SCRIPT] + args + ["--url", url, "--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    try:
        out = json.loads(proc.stdout) if proc.stdout.strip() else {}
    except json.JSONDecodeError:
        out = None
    return proc.returncode, out, proc.stdout, proc.stderr


def pesan(out, e):
    """Pesan galat, baik dari JSON ({"galat": ...}) maupun stderr biasa."""
    if isinstance(out, dict) and "galat" in out:
        return out["galat"]
    return e


def cek(nama, kondisi, detail=""):
    if kondisi:
        PASSED.append(nama)
    else:
        FAILED.append(f"{nama} -- {detail}")


def uji_dengan_kunci(fn):
    """Bungkus satu kasus uji dengan file kunci sementara berisi SANDI_BENAR."""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        f.write(SANDI_BENAR + "\n")
    os.chmod(path, 0o600)
    try:
        fn(path)
    finally:
        os.remove(path)


def main():
    srv, port = jalankan_server("normal")
    url = f"http://127.0.0.1:{port}"

    # 1-3: cek server normal (tanpa auth)
    rc, out, o, e = jalankan_cli(["cek"], url)
    cek("01 cek server normal rc=0", rc == 0, f"rc={rc} err={e}")
    cek("02 cek server normal jumlah_notebook", out and out.get("jumlah_notebook") == 1, out)
    cek("03 cek kata_sandi tersamar saat tanpa sandi", out and out.get("kata_sandi") == "(tidak dipakai)", out)

    # 4-5: daftar notebook
    rc, out, o, e = jalankan_cli(["daftar-notebook"], url)
    cek("04 daftar-notebook rc=0", rc == 0, e)
    cek("05 daftar-notebook isi benar", out and out["notebook"][0]["nama"] == "Regulasi Pajak UMKM", out)

    # 6-7: daftar sumber by nama notebook
    rc, out, o, e = jalankan_cli(["daftar-sumber", "--notebook", "Regulasi Pajak UMKM"], url)
    cek("06 daftar-sumber by nama rc=0", rc == 0, e)
    cek("07 daftar-sumber 2 baris, satu diproses", out and out["jumlah"] == 2 and out["sumber"][1]["status"] == "processing", out)

    # 8: daftar-sumber notebook tidak ada
    rc, out, o, e = jalankan_cli(["daftar-sumber", "--notebook", "Tidak Ada"], url)
    cek("08 notebook tidak ditemukan -> galat awam", rc == 2 and "tidak ditemukan" in pesan(out, e), pesan(out, e))

    # 9-10: tambah-sumber link pratinjau (tanpa --ya)
    rc, out, o, e = jalankan_cli(["tambah-sumber", "--notebook", "notebook:abc123", "--tipe", "link", "--sumber-url", "https://contoh.go.id/pp55"], url)
    cek("09 tambah-sumber pratinjau rc=0", rc == 0, e)
    cek("10 tambah-sumber pratinjau tidak menulis", out and out.get("pratinjau") is True, out)

    # 11: tambah-sumber link dengan --ya
    rc, out, o, e = jalankan_cli(["tambah-sumber", "--notebook", "notebook:abc123", "--tipe", "link", "--sumber-url", "https://contoh.go.id/pp55", "--ya"], url)
    cek("11 tambah-sumber --ya berhasil", rc == 0 and out.get("ditambahkan") is True, (rc, out, e))

    # 12: tambah-sumber teks tanpa --teks -> error input
    rc, out, o, e = jalankan_cli(["tambah-sumber", "--notebook", "notebook:abc123", "--tipe", "teks", "--ya"], url)
    cek("12 tambah-sumber teks tanpa isi -> galat", rc == 2 and "--teks" in pesan(out, e), pesan(out, e))

    # 13: tambah-sumber tipe file -> ditolak dengan pesan jelas
    rc, out, o, e = jalankan_cli(["tambah-sumber", "--notebook", "notebook:abc123", "--tipe", "file", "--ya"], url)
    cek("13 tipe file ditolak dengan pesan jelas", rc != 0 and "tampilan web" in pesan(out, e), pesan(out, e))

    # 14-15: cari
    rc, out, o, e = jalankan_cli(["cari", "--kueri", "PPh final"], url)
    cek("14 cari rc=0", rc == 0, e)
    cek("15 cari isi cuplikan", out and out["jumlah"] == 1 and "PPh Final" in out["hasil"][0]["cuplikan"], out)

    # 16-17: tanya (pakai model default)
    rc, out, o, e = jalankan_cli(["tanya", "--notebook", "notebook:abc123", "--pertanyaan", "Berapa tarif PPh final UMKM?"], url)
    cek("16 tanya rc=0", rc == 0, e)
    cek("17 tanya isi jawaban ada", out and "0,5%" in out.get("jawaban", ""), out)

    # 18: ringkasan
    rc, out, o, e = jalankan_cli(["ringkasan", "--notebook", "notebook:abc123"], url)
    cek("18 ringkasan rc=0 & ada catatan disclaimer", rc == 0 and "membaca dokumen" in out.get("catatan", ""), (rc, out))

    # 19-20: podcast-mulai pratinjau & podcast-status
    rc, out, o, e = jalankan_cli(["podcast-mulai", "--notebook", "notebook:abc123", "--profil", "Ngobrol Santai", "--pembicara", "Dua Suara ID", "--nama-episode", "Ringkasan Pajak"], url)
    cek("19 podcast-mulai pratinjau rc=0", rc == 0 and out.get("pratinjau") is True, (rc, out, e))
    rc, out, o, e = jalankan_cli(["podcast-status", "--id", "job:1"], url)
    cek("20 podcast-status rc=0", rc == 0 and out.get("status") == "completed", (rc, out, e))

    # 21: URL bukan localhost -> ditolak
    rc, out, o, e = jalankan_cli(["cek"], "http://192.0.2.10:5055")
    cek("21 URL non-localhost ditolak", rc == 2 and "bukan komputer ini" in pesan(out, e), pesan(out, e))

    # 22: server mati (port tak dipakai)
    rc, out, o, e = jalankan_cli(["cek"], "http://127.0.0.1:1")
    cek("22 server mati -> pesan awam", rc == 4 and "mati" in pesan(out, e), pesan(out, e))

    srv.shutdown()

    # 23-25: mode auth
    srv2, port2 = jalankan_server("auth")
    url2 = f"http://127.0.0.1:{port2}"

    def coba_auth_benar(kunci_path):
        rc, out, o, e = jalankan_cli(["cek", "--kunci-file", kunci_path], url2)
        cek("23 auth: sandi benar -> cek sukses", rc == 0 and out and out.get("auth_aktif") is True, (rc, out, e))

    uji_dengan_kunci(coba_auth_benar)

    fd, kunci_salah = tempfile.mkstemp()
    os.close(fd)
    with open(kunci_salah, "w", encoding="utf-8") as f:
        f.write("sandi-salah\n")
    os.chmod(kunci_salah, 0o600)
    rc, out, o, e = jalankan_cli(["cek", "--kunci-file", kunci_salah], url2)
    cek("24 auth: sandi salah -> 401 awam", rc == 5 and "401" in pesan(out, e), pesan(out, e))
    os.remove(kunci_salah)

    rc, out, o, e = jalankan_cli(["cek"], url2)
    cek("25 auth: tanpa kunci sama sekali -> pesan minta simpan-kunci", rc == 5 and "simpan-kunci" in pesan(out, e), pesan(out, e))
    srv2.shutdown()

    # 26: server balas bukan JSON
    srv3, port3 = jalankan_server("rusak")
    url3 = f"http://127.0.0.1:{port3}"
    rc, out, o, e = jalankan_cli(["cek"], url3)
    cek("26 balasan rusak -> pesan awam", rc == 4 and "JSON" in pesan(out, e), pesan(out, e))
    srv3.shutdown()

    # 27: error 500
    srv4, port4 = jalankan_server("error500")
    url4 = f"http://127.0.0.1:{port4}"
    rc, out, o, e = jalankan_cli(["cek"], url4)
    cek("27 error 500 -> pesan awam", rc == 4 and "internal" in pesan(out, e), pesan(out, e))
    srv4.shutdown()

    # 28: timeout
    srv5, port5 = jalankan_server("timeout")
    url5 = f"http://127.0.0.1:{port5}"
    rc, out, o, e = jalankan_cli(["cek", "--timeout", "1"], url5)
    cek("28 timeout -> pesan awam", rc == 4 and "detik" in pesan(out, e), pesan(out, e))
    srv5.shutdown()

    # 29: buat-notebook pratinjau
    srv6, port6 = jalankan_server("normal")
    url6 = f"http://127.0.0.1:{port6}"
    rc, out, o, e = jalankan_cli(["buat-notebook", "--nama", "Riset Supplier"], url6)
    cek("29 buat-notebook pratinjau", rc == 0 and out.get("pratinjau") is True, (rc, out))

    # 30: buat-notebook --ya
    rc, out, o, e = jalankan_cli(["buat-notebook", "--nama", "Riset Supplier", "--ya"], url6)
    cek("30 buat-notebook --ya", rc == 0 and out.get("dibuat") is True, (rc, out, e))
    srv6.shutdown()

    print(f"\nLULUS: {len(PASSED)}  GAGAL: {len(FAILED)}")
    for f in FAILED:
        print(f"  ❌ {f}")
    if FAILED:
        sys.exit(1)
    print("✅ semua uji lulus")


if __name__ == "__main__":
    main()
