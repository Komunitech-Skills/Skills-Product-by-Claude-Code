#!/usr/bin/env python3
"""Perekam jawaban Umami ASLI untuk uji regresi (hanya pengembang Komunitech).

Menjalankan perantara HTTP di 127.0.0.1:<port> yang meneruskan setiap permintaan ke Umami asli dan menyimpan
jawabannya ke tests/fixtures/umami-3.4.0.json dengan kunci 'METODE path?query' per peran kunci:
  baca  = kunci API akun view-only (anggota tim 'team-view-only')
  admin = kunci API akun admin (melihat 2 website -> uji pilihan ganda)
  lain  = kunci salah
Kunci API TIDAK disimpan: peran ditentukan dari file kunci yang diberikan, dan field 'token' pada /api/me
serta 'accessCode' tim diganti '***'.

  python3 tests/rekam_fixture.py --kunci-baca F1 --kunci-admin F2 --detik 120
"""
import argparse
import json
import os
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SINI = os.path.dirname(os.path.abspath(__file__))
KELUAR = os.path.join(SINI, "fixtures", "umami-3.4.0.json")


def bersihkan(o):
    if isinstance(o, dict):
        return {k: ("***" if k in ("token", "accessCode", "key", "partialToken") else bersihkan(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [bersihkan(x) for x in o]
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asli", default="http://127.0.0.1:3000")
    ap.add_argument("--port", type=int, default=3996)
    ap.add_argument("--kunci-baca", required=True)
    ap.add_argument("--kunci-admin", required=True)
    ap.add_argument("--detik", type=int, default=120)
    a = ap.parse_args()
    peran = {open(a.kunci_baca).read().strip(): "baca", open(a.kunci_admin).read().strip(): "admin"}
    rekaman = {}
    if os.path.exists(KELUAR):
        rekaman = json.load(open(KELUAR, encoding="utf-8")).get("rekaman", {})
    buka = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    kunci_lock = threading.Lock()

    class H(BaseHTTPRequestHandler):
        def log_message(self, *x):
            pass

        def _terus(self):
            n = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(n) if n else None
            auth = self.headers.get("Authorization") or ""
            tok = auth[7:] if auth.startswith("Bearer ") else ""
            p = peran.get(tok, "lain" if tok else "tanpa")
            req = urllib.request.Request(a.asli + self.path, data=body, method=self.command)
            for h in ("Authorization", "Content-Type", "Accept"):
                if self.headers.get(h):
                    req.add_header(h, self.headers[h])
            try:
                with buka.open(req, timeout=30) as r:
                    kode, isi = r.status, r.read()
            except urllib.error.HTTPError as e:
                kode, isi = e.code, e.read()
            try:
                j = json.loads(isi) if isi else None
            except ValueError:
                j = None
            if not (self.command == "POST" and self.path.startswith("/api/auth/login")):
                with kunci_lock:
                    rekaman.setdefault(p, {})[f"{self.command} {self.path}"] = [kode, bersihkan(j)]
            self.send_response(kode)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(isi)))
            self.end_headers()
            self.wfile.write(isi)

        do_GET = do_POST = _terus

    srv = ThreadingHTTPServer(("127.0.0.1", a.port), H)
    threading.Timer(a.detik, srv.shutdown).start()
    print(f"merekam di http://127.0.0.1:{a.port} selama {a.detik} detik ...", flush=True)
    srv.serve_forever()
    os.makedirs(os.path.dirname(KELUAR), exist_ok=True)
    with open(KELUAR, "w", encoding="utf-8") as f:
        json.dump({"sumber": "Umami 3.4.0 (image resmi ghcr.io/umami-software/umami:3.4.0, PostgreSQL 15) di "
                             "127.0.0.1, data fiktif tests/isi_data_fiktif.py, direkam 2026-09-29",
                   "rekaman": rekaman}, f, ensure_ascii=False, indent=0, sort_keys=True)
    print(f"tersimpan {sum(len(v) for v in rekaman.values())} jawaban -> {KELUAR}")


if __name__ == "__main__":
    main()
