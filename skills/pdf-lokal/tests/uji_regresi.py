#!/usr/bin/env python3
"""Uji regresi scripts/pdf.py memakai SERVER TIRUAN lokal (http.server bawaan Python),
bukan Stirling-PDF sungguhan - supaya bisa dijalankan tanpa memasang apa pun.

Respons server tiruan disusun meniru bentuk nyata Stirling-PDF v2.14.3 (header
Content-Type/Content-Disposition, bentuk error JSON) yang sudah diverifikasi langsung
ke server Stirling-PDF sungguhan (Docker, ghcr.io/stirling-tools/stirling-pdf:latest,
versi 2.14.3) saat skill ini dibuat - lihat references/sumber-api-stirling.md.

Jalankan: python3 uji_regresi.py   (keluar 0 bila semua lulus)
"""
import http.server
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import zipfile
from pathlib import Path

SINI = Path(__file__).resolve().parent
SCRIPT = SINI.parent / "scripts" / "pdf.py"

PDF_MINIMAL = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 300]>>endobj\n"
    b"trailer<</Size 4/Root 1 0 R>>\n%%EOF"
)


def buat_zip_dummy():
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("halaman_1.pdf", PDF_MINIMAL)
        z.writestr("halaman_2.pdf", PDF_MINIMAL)
    return buf.getvalue()


class TiruanStirlingHandler(http.server.BaseHTTPRequestHandler):
    server_version = "TiruanStirling/1.0"
    panggilan = []  # dicatat oleh kelas untuk pengecekan urutan panggilan

    def log_message(self, fmt, *args):
        pass  # diam - jangan penuhi output uji

    def _kirim_pdf(self, nama_file, isi=PDF_MINIMAL):
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", f'form-data; name="attachment"; filename="{nama_file}"')
        self.send_header("Content-Length", str(len(isi)))
        self.end_headers()
        self.wfile.write(isi)

    def _kirim_zip(self, nama_file):
        isi = buat_zip_dummy()
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f'form-data; name="attachment"; filename="{nama_file}"')
        self.send_header("Content-Length", str(len(isi)))
        self.end_headers()
        self.wfile.write(isi)

    def _kirim_json(self, status, payload):
        isi = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(isi)))
        self.end_headers()
        self.wfile.write(isi)

    def do_GET(self):
        TiruanStirlingHandler.panggilan.append(("GET", self.path))
        if self.path == "/api/v1/info/status":
            self._kirim_json(200, {"version": "2.14.3-tiruan", "status": "UP"})
        elif self.path == "/api/v1/ui-data/ocr-pdf":
            self._kirim_json(200, {"languages": ["eng", "fra", "deu"]})  # 'ind' sengaja tidak ada
        else:
            self._kirim_json(404, {"detail": f"No endpoint found for GET {self.path}", "status": 404})

    def do_POST(self):
        panjang = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(panjang)
        TiruanStirlingHandler.panggilan.append(("POST", self.path))

        if self.path == "/api/v1/general/merge-pdfs":
            return self._kirim_pdf("hasil_merged.pdf")
        if self.path == "/api/v1/general/split-pages":
            return self._kirim_zip("hasil_split.zip")
        if self.path == "/api/v1/general/rearrange-pages":
            return self._kirim_pdf("hasil_rearranged.pdf")
        if self.path == "/api/v1/misc/compress-pdf":
            return self._kirim_pdf("hasil_compress.pdf", isi=PDF_MINIMAL[:60])  # pura2 lebih kecil
        if self.path == "/api/v1/misc/ocr-pdf":
            if b'name="languages"\r\n\r\nind' in body and b'name="languages"\r\n\r\neng' not in body:
                return self._kirim_json(500, {"error": "Job failed: java.io.IOException: Invalid OCR "
                                                         "languages format: none of the selected languages "
                                                         "are valid"})
            return self._kirim_pdf("hasil_ocr.pdf")
        if self.path == "/api/v1/convert/img/pdf":
            return self._kirim_pdf("hasil_img.pdf")
        if self.path == "/api/v1/general/rotate-pdf":
            return self._kirim_pdf("hasil_rotate.pdf")
        if self.path == "/api/v1/security/add-watermark":
            return self._kirim_pdf("hasil_watermark.pdf")
        if self.path == "/api/v1/security/add-password":
            return self._kirim_pdf("hasil_locked.pdf")
        if self.path == "/api/v1/security/remove-password":
            if b"password" in body and b"salah" in body:
                return self._kirim_json(400, {
                    "detail": "The PDF Document is passworded and either the password was not "
                              "provided or was incorrect",
                    "status": 400, "title": "PDF Password Required", "errorCode": "E004",
                })
            return self._kirim_pdf("hasil_unlocked.pdf")
        if self.path == "/api/v1/general/multi-page-layout":
            return self._kirim_pdf("hasil_layout.pdf")
        self._kirim_json(404, {"detail": f"No endpoint found for POST {self.path}", "status": 404})


def port_bebas():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def jalankan(args, env_tambahan=None, cwd=None):
    env = dict(os.environ)
    env.update(env_tambahan or {})
    r = subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True,
                        encoding="utf-8", env=env, cwd=cwd)
    return r.returncode, r.stdout, r.stderr


def main():
    gagal = 0
    total = 0

    port = port_bebas()
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), TiruanStirlingHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base_env = {"STIRLING_URL": f"http://127.0.0.1:{port}"}

    tmp = Path(tempfile.mkdtemp(prefix="uji-pdf-lokal-"))
    try:
        f1 = tmp / "resi1.pdf"
        f2 = tmp / "resi2.pdf"
        f1.write_bytes(PDF_MINIMAL)
        f2.write_bytes(PDF_MINIMAL)
        foto = tmp / "nota.png"
        foto.write_bytes(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00"
            b"\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb0"
            b"\x00\x00\x00\x00IEND\xaeB`\x82"
        )

        def cek(nama, kondisi, keterangan=""):
            nonlocal gagal, total
            total += 1
            if not kondisi:
                gagal += 1
                print(f"GAGAL [{nama}] {keterangan}")
            else:
                print(f"lulus [{nama}]")

        # --- 1. Skenario normal: cek server ---
        rc, out, err = jalankan(["cek"], base_env)
        cek("cek-normal", rc == 0 and "2.14.3-tiruan" in out, f"rc={rc} out={out!r} err={err!r}")

        # --- 2. Skenario normal: gabung ---
        rc, out, err = jalankan(["gabung", str(f1), str(f2)], base_env, cwd=str(tmp))
        keluar = tmp / "resi1-gabungan.pdf"
        cek("gabung-normal", rc == 0 and keluar.is_file() and keluar.read_bytes() == PDF_MINIMAL,
            f"rc={rc} out={out!r} err={err!r}")

        # --- 3. Skenario normal: pisah-halaman (respons zip -> jadi folder berisi file) ---
        rc, out, err = jalankan(["pisah-halaman", str(f1)], base_env, cwd=str(tmp))
        folder = tmp / "resi1-per-halaman"
        isi_folder = sorted(p.name for p in folder.glob("*.pdf")) if folder.is_dir() else []
        cek("pisah-halaman-normal", rc == 0 and isi_folder == ["halaman_1.pdf", "halaman_2.pdf"],
            f"rc={rc} out={out!r} err={err!r} isi={isi_folder}")

        # --- 4. Input tidak lengkap: gabung dengan 1 file saja ---
        rc, out, err = jalankan(["gabung", str(f1)], base_env, cwd=str(tmp))
        cek("gabung-input-kurang", rc != 0 and "minimal 2 file" in err, f"rc={rc} err={err!r}")

        # --- 5. Di luar cakupan: file tidak ada ---
        rc, out, err = jalankan(["kompres", str(tmp / "tidak-ada.pdf")], base_env, cwd=str(tmp))
        cek("file-tidak-ada", rc != 0 and "tidak ditemukan" in err, f"rc={rc} err={err!r}")

        # --- Tambahan: server mati / tidak bisa dihubungi ---
        rc, out, err = jalankan(["cek"], {"STIRLING_URL": "http://127.0.0.1:1"}, cwd=str(tmp))
        cek("server-mati", rc != 0 and "Tidak bisa menghubungi" in err, f"rc={rc} err={err!r}")

        # --- Tambahan: OCR minta bahasa 'ind' yang belum terpasang -> fallback otomatis ke eng ---
        rc, out, err = jalankan(["ocr", str(f1), "--keluaran", str(tmp / "hasil-ocr.pdf")], base_env,
                                 cwd=str(tmp))
        cek("ocr-fallback-bahasa", rc == 0 and "ind belum terpasang" in out and (tmp / "hasil-ocr.pdf").is_file(),
            f"rc={rc} out={out!r} err={err!r}")

        # --- Tambahan: buka-kunci dengan sandi salah -> pesan ramah, bukan traceback ---
        rc, out, err = jalankan(["buka-kunci", str(f1), "--sandi", "salah"], base_env, cwd=str(tmp))
        cek("sandi-salah", rc != 0 and "kata sandi" in err.lower() and "Traceback" not in err,
            f"rc={rc} err={err!r}")

        # --- Tambahan: URL non-lokal ditolak tanpa STIRLING_ALLOW_REMOTE ---
        rc, out, err = jalankan(["cek"], {"STIRLING_URL": "http://203.0.113.5:8080"}, cwd=str(tmp))
        cek("tolak-url-remote", rc != 0 and "STIRLING_ALLOW_REMOTE" in err, f"rc={rc} err={err!r}")

        # --- Tambahan: rapikan-resi banyak file (merge lalu multi-page-layout, urutan panggilan API) ---
        TiruanStirlingHandler.panggilan.clear()
        rc, out, err = jalankan(
            ["rapikan-resi", str(f1), str(f2), "--per-lembar", "4", "--keluaran", str(tmp / "resi-rapi.pdf")],
            base_env, cwd=str(tmp))
        urutan = [p for _, p in TiruanStirlingHandler.panggilan]
        cek("rapikan-resi-multi-file", rc == 0 and (tmp / "resi-rapi.pdf").is_file()
            and "/api/v1/general/merge-pdfs" in urutan and "/api/v1/general/multi-page-layout" in urutan,
            f"rc={rc} out={out!r} err={err!r} urutan={urutan}")

        # --- Tambahan: rotate dengan sudut tidak valid ditolak di sisi client (tanpa panggil server) ---
        rc, out, err = jalankan(["putar", str(f1), "--derajat", "45"], base_env, cwd=str(tmp))
        cek("derajat-tidak-valid", rc != 0, f"rc={rc} err={err!r}")

        # --- Tambahan: foto ke PDF ---
        rc, out, err = jalankan(["foto-ke-pdf", str(foto), "--keluaran", str(tmp / "nota.pdf")], base_env,
                                 cwd=str(tmp))
        cek("foto-ke-pdf-normal", rc == 0 and (tmp / "nota.pdf").is_file(), f"rc={rc} out={out!r} err={err!r}")

    finally:
        httpd.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{total - gagal}/{total} skenario lulus.")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
