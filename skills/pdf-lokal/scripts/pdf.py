#!/usr/bin/env python3
"""pdf-lokal (Komunitech) - olah PDF lewat Stirling-PDF yang terpasang di komputer pembeli.

Script ini TIDAK memproses PDF sendiri. Ia memanggil REST API lokal Stirling-PDF
(default http://localhost:8080) yang harus sudah terpasang & berjalan di komputer
yang sama (lihat docs/panduan-stirling-pdf.md). Hanya library standar Python 3.8+,
lintas OS (Windows/macOS/Linux), tanpa paket tambahan.

Alamat server & kunci API (opsional, hanya bila keamanan Stirling-PDF diaktifkan):
  ENV STIRLING_URL       (default: http://localhost:8080)
  ENV STIRLING_API_KEY   (default: kosong / tidak dipakai)
  ENV STIRLING_ALLOW_REMOTE=1  (WAJIB diisi bila STIRLING_URL bukan localhost/127.0.0.1 -
                                 penegasan eksplisit bahwa pengguna sadar file akan dikirim
                                 ke alamat itu, bukan ke komputer sendiri)

Contoh:
  python3 pdf.py cek
  python3 pdf.py gabung nota1.pdf nota2.pdf
  python3 pdf.py pisah-halaman kontrak.pdf
  python3 pdf.py pisah-rentang laporan.pdf --halaman 3-7
  python3 pdf.py kompres foto-nota.pdf --level 6
  python3 pdf.py ocr scan-invoice.pdf --bahasa ind eng
  python3 pdf.py foto-ke-pdf nota1.jpg nota2.jpg --keluaran kumpulan-nota.pdf
  python3 pdf.py putar dokumen.pdf --derajat 90
  python3 pdf.py watermark draf-kontrak.pdf --teks "DRAF - BELUM SAH"
  python3 pdf.py kunci laporan-gaji.pdf --sandi rahasia123
  python3 pdf.py buka-kunci laporan-gaji.pdf --sandi rahasia123
  python3 pdf.py rapikan-resi resi1.pdf resi2.pdf resi3.pdf resi4.pdf --per-lembar 4

Referensi endpoint & parameter: lihat references/sumber-api-stirling.md (diambil dari
Swagger /v1/api-docs server Stirling-PDF v2.14.3 yang sungguhan dijalankan untuk
memverifikasi script ini, tanggal akses tercatat di file tsb).
"""
import argparse
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from pathlib import Path

VERSI = "1.0.0"
APLIKASI = "pdf-lokal"
LOKAL_DIIZINKAN = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}


class Gagal(Exception):
    """Error yang pesannya aman & jelas untuk ditampilkan ke pengguna awam."""


# ---------------------------------------------------------------------------
# Konfigurasi & keamanan alamat server
# ---------------------------------------------------------------------------

def ambil_base_url(arg_url=None):
    url = (arg_url or os.environ.get("STIRLING_URL") or "http://localhost:8080").rstrip("/")
    host = urllib.parse.urlparse(url).hostname or ""
    if host not in LOKAL_DIIZINKAN and os.environ.get("STIRLING_ALLOW_REMOTE") != "1":
        raise Gagal(
            f"Alamat Stirling-PDF ({url}) bukan localhost/127.0.0.1. Skill ini dirancang untuk "
            "memproses file HANYA di komputer sendiri. Jika kamu memang sengaja memakai server "
            "lain (mis. server kantor di jaringan lokal) dan paham risikonya (file dikirim ke "
            "alamat itu), set environment variable STIRLING_ALLOW_REMOTE=1 lalu coba lagi."
        )
    return url


def ambil_api_key(arg_key=None):
    return arg_key or os.environ.get("STIRLING_API_KEY") or ""


# ---------------------------------------------------------------------------
# Multipart/form-data manual (tanpa dependensi luar) + panggilan HTTP
# ---------------------------------------------------------------------------

def _tebak_tipe(nama_file):
    tipe, _ = mimetypes.guess_type(nama_file)
    return tipe or "application/octet-stream"


def bangun_multipart(field_biasa, field_file):
    """field_biasa: list[(nama, nilai)] (urutan dijaga, boleh nama berulang untuk array).
    field_file: list[(nama, path_lokal)] (boleh nama berulang, mis. beberapa fileInput)."""
    boundary = uuid.uuid4().hex
    baris = []
    for nama, nilai in field_biasa:
        baris.append(f"--{boundary}\r\n".encode())
        baris.append(f'Content-Disposition: form-data; name="{nama}"\r\n\r\n'.encode())
        baris.append(str(nilai).encode("utf-8") + b"\r\n")
    for nama, path in field_file:
        p = Path(path)
        nama_file = p.name
        baris.append(f"--{boundary}\r\n".encode())
        baris.append(
            f'Content-Disposition: form-data; name="{nama}"; filename="{nama_file}"\r\n'.encode()
        )
        baris.append(f"Content-Type: {_tebak_tipe(nama_file)}\r\n\r\n".encode())
        baris.append(p.read_bytes() + b"\r\n")
    baris.append(f"--{boundary}--\r\n".encode())
    body = b"".join(baris)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


def _pesan_dari_json(mentah):
    try:
        data = json.loads(mentah.decode("utf-8", errors="replace"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    if isinstance(data, dict):
        for kunci in ("detail", "error", "message"):
            if data.get(kunci):
                return str(data[kunci])
    return None


def panggil_stirling(base_url, api_key, path, field_biasa=None, field_file=None, method="POST", timeout=180):
    """Kembalikan (content_type, nama_saran, isi_bytes). Melempar Gagal dengan pesan ramah."""
    url = base_url + path
    headers = {}
    if api_key:
        headers["X-API-KEY"] = api_key
    body = None
    if method == "POST":
        body, ctype = bangun_multipart(field_biasa or [], field_file or [])
        headers["Content-Type"] = ctype
        headers["Content-Length"] = str(len(body))
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            isi = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            cd = resp.headers.get("Content-Disposition", "")
            nama_saran = None
            if 'filename="' in cd:
                nama_saran = cd.split('filename="', 1)[1].split('"', 1)[0]
            return ctype, nama_saran, isi
    except urllib.error.HTTPError as e:
        mentah = e.read()
        pesan = _pesan_dari_json(mentah) or mentah.decode("utf-8", errors="replace")[:300]
        if e.code == 401:
            raise Gagal(
                "Stirling-PDF menolak permintaan (401 - butuh login/API key). Server ini punya "
                "keamanan aktif. Ambil API key dari aplikasi Stirling-PDF (Account/Pengaturan > "
                "API Key) lalu set ENV STIRLING_API_KEY, atau matikan login untuk pemakaian "
                "pribadi (lihat docs/panduan-stirling-pdf.md bagian Keamanan)."
            ) from None
        if e.code == 404:
            raise Gagal(
                f"Endpoint '{path}' tidak ditemukan di server Stirling-PDF ini (404). Kemungkinan "
                "versi Stirling-PDF yang terpasang lebih lama dan belum punya fitur ini, atau "
                "fitur ini masuk kelompok berbayar/proprietary yang tidak diaktifkan. Jalankan "
                "'python3 pdf.py cek' untuk melihat versi, lalu perbarui Stirling-PDF bila perlu."
            ) from None
        if e.code == 400 and ("password" in pesan.lower() or "E004" in pesan):
            raise Gagal(
                "PDF ini terkunci kata sandi, atau kata sandi yang diberikan salah. Kalau baru "
                "memakai perintah 'buka-kunci', coba periksa lagi ejaan/besar-kecil hurufnya. "
                "Kalau belum, buka dulu dengan 'buka-kunci --sandi ...' (pakai kata sandi yang "
                "benar), baru proses lagi."
            ) from None
        if e.code == 400:
            raise Gagal(f"Stirling-PDF menolak permintaan ini: {pesan}") from None
        if e.code == 413:
            raise Gagal(
                "File terlalu besar untuk diproses Stirling-PDF (413). Coba kompres dulu "
                "('python3 pdf.py kompres ...') atau perbesar batas ukuran unggah di "
                "Pengaturan Stirling-PDF (System > File Upload Limit), lalu coba lagi."
            ) from None
        if e.code == 500:
            raise Gagal(
                f"Stirling-PDF gagal memproses file ini: {pesan}. Biasanya artinya file rusak, "
                "bukan PDF yang valid, atau formatnya tidak didukung. Coba perintah "
                "'python3 pdf.py cek' dulu untuk pastikan server sehat, dan periksa file aslinya "
                "bisa dibuka normal."
            ) from None
        raise Gagal(f"Stirling-PDF membalas error ({e.code}): {pesan}") from None
    except urllib.error.URLError as e:
        raise Gagal(
            f"Tidak bisa menghubungi Stirling-PDF di {base_url} ({e.reason}). Pastikan aplikasi "
            "Stirling-PDF sudah dibuka & sedang berjalan di komputer ini. Lihat "
            "docs/panduan-stirling-pdf.md untuk cara memasang dan menyalakannya, atau ikuti "
            "'Cara manual tanpa script' di SKILL.md bila belum sempat memasangnya."
        ) from None
    except TimeoutError:
        raise Gagal(
            "Stirling-PDF tidak merespons dalam waktu wajar (timeout). File mungkin terlalu besar "
            "atau prosesnya berat (mis. OCR file banyak halaman). Coba file yang lebih kecil dulu, "
            "atau ulangi setelah beberapa saat."
        ) from None


# ---------------------------------------------------------------------------
# Path keluaran: selalu di sebelah file asli, tidak pernah menimpa
# ---------------------------------------------------------------------------

def path_keluaran_aman(diinginkan):
    """Kembalikan Path yang belum ada; tambah (1), (2), ... bila sudah dipakai."""
    p = Path(diinginkan)
    if not p.exists():
        return p
    n = 1
    while True:
        kandidat = p.with_name(f"{p.stem}({n}){p.suffix}")
        if not kandidat.exists():
            return kandidat
        n += 1


def keluaran_default_tunggal(file_asli, akhiran, ekstensi=".pdf"):
    p = Path(file_asli)
    return path_keluaran_aman(p.with_name(f"{p.stem}{akhiran}{ekstensi}"))


def keluaran_default_banyak(file_pertama, nama):
    p = Path(file_pertama)
    return path_keluaran_aman(p.parent / nama)


def simpan_hasil(isi_bytes, ctype, nama_saran, path_tujuan):
    """Simpan hasil dari Stirling. Bila zip (banyak file keluaran), ekstrak ke folder."""
    adalah_zip = (nama_saran or "").lower().endswith(".zip")
    if adalah_zip:
        folder = Path(path_tujuan)
        if folder.suffix:
            folder = folder.with_suffix("")
        folder = path_keluaran_aman(folder)
        folder.mkdir(parents=True, exist_ok=True)
        tmp_zip = folder.parent / (folder.name + ".zip.tmp")
        tmp_zip.write_bytes(isi_bytes)
        daftar = []
        with zipfile.ZipFile(tmp_zip) as z:
            for info in z.infolist():
                z.extract(info, folder)
                daftar.append(str(folder / info.filename))
        tmp_zip.unlink(missing_ok=True)
        return folder, daftar
    tujuan = Path(path_tujuan)
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    tujuan.write_bytes(isi_bytes)
    return tujuan, [str(tujuan)]


def periksa_file_ada(*paths):
    hilang = [p for p in paths if not Path(p).is_file()]
    if hilang:
        raise Gagal("File tidak ditemukan: " + ", ".join(hilang))


# ---------------------------------------------------------------------------
# Perintah
# ---------------------------------------------------------------------------

def cmd_cek(args):
    base = ambil_base_url(args.url)
    ctype, _nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/info/status", method="GET")
    try:
        data = json.loads(isi.decode("utf-8"))
    except json.JSONDecodeError:
        raise Gagal("Server membalas tapi bukan format yang dikenali. Cek URL Stirling-PDF-mu.")
    print(f"Stirling-PDF HIDUP di {base}")
    print(f"  Versi  : {data.get('version', '(tidak diketahui)')}")
    print(f"  Status : {data.get('status', '(tidak diketahui)')}")
    print("Siap dipakai. Coba: python3 pdf.py gabung file1.pdf file2.pdf")


def cmd_gabung(args):
    periksa_file_ada(*args.file)
    if len(args.file) < 2:
        raise Gagal("Butuh minimal 2 file PDF untuk digabung.")
    base = ambil_base_url(args.url)
    field_file = [("fileInput", f) for f in args.file]
    field_biasa = [
        ("sortType", args.urutan),
        ("removeCertSign", "true"),
        ("generateToc", "false"),
    ]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/general/merge-pdfs",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_banyak(
        args.file[0], f"{Path(args.file[0]).stem}-gabungan.pdf")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil digabung ({len(args.file)} file) -> {hasil.resolve()}")


def cmd_pisah_halaman(args):
    periksa_file_ada(args.file)
    base = ambil_base_url(args.url)
    field_biasa = [("pageNumbers", "all")]
    field_file = [("fileInput", args.file)]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/general/split-pages",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran_folder) if args.keluaran_folder else keluaran_default_banyak(
        args.file, f"{Path(args.file).stem}-per-halaman")
    folder, daftar = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil dipisah per halaman -> folder {folder.resolve()}")
    for f in daftar:
        print(f"  - {f}")


def cmd_pisah_rentang(args):
    periksa_file_ada(args.file)
    base = ambil_base_url(args.url)
    field_biasa = [("pageNumbers", args.halaman), ("customMode", "CUSTOM")]
    field_file = [("fileInput", args.file)]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/general/rearrange-pages",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_tunggal(
        args.file, f"-hal-{args.halaman.replace(',', '_')}")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil diambil halaman {args.halaman} -> {hasil.resolve()}")


def cmd_kompres(args):
    periksa_file_ada(args.file)
    if not (1 <= args.level <= 9):
        raise Gagal("--level harus 1-9 (1 = kompres ringan/kualitas terbaik, 9 = kompres maksimal).")
    base = ambil_base_url(args.url)
    field_biasa = [
        ("optimizeLevel", str(args.level)),
        ("expectedOutputSize", args.target or "10MB"),
        ("linearize", "false"),
        ("normalize", "false"),
        ("grayscale", "true" if args.hitam_putih else "false"),
        ("lineArt", "false"),
        ("lineArtThreshold", "55"),
        ("lineArtEdgeLevel", "1"),
    ]
    field_file = [("fileInput", args.file)]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/misc/compress-pdf",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_tunggal(args.file, "-kompres")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    ukuran_awal = Path(args.file).stat().st_size
    ukuran_akhir = hasil.stat().st_size
    print(f"Berhasil dikompres: {ukuran_awal/1024:.0f} KB -> {ukuran_akhir/1024:.0f} KB")
    print(f"  -> {hasil.resolve()}")


def cmd_ocr(args):
    periksa_file_ada(args.file)
    base = ambil_base_url(args.url)
    api_key = ambil_api_key(args.api_key)
    field_file = [("fileInput", args.file)]

    def coba(bahasa_list):
        field_biasa = [("languages", b) for b in bahasa_list]
        field_biasa += [
            ("ocrType", args.tipe),
            ("ocrRenderType", "hocr"),
            ("sidecar", "false"),
            ("deskew", "false"),
            ("clean", "false"),
            ("cleanFinal", "false"),
            ("removeImagesAfter", "false"),
        ]
        return panggil_stirling(base, api_key, "/api/v1/misc/ocr-pdf", field_biasa, field_file)

    bahasa_diminta = args.bahasa or ["ind", "eng"]
    bahasa_dipakai = bahasa_diminta
    # Cek dulu bahasa apa saja yang benar-benar terpasang, supaya tidak diam-diam
    # memakai bahasa Inggris saja padahal pengguna kira sudah pakai bahasa Indonesia.
    try:
        _ctype, _nama, isi_bhs = panggil_stirling(base, api_key, "/api/v1/ui-data/ocr-pdf", method="GET")
        tersedia = json.loads(isi_bhs).get("languages") or []
    except Exception:
        tersedia = None
    if tersedia:
        bahasa_dipakai = [b for b in bahasa_diminta if b in tersedia]
        dilewati = [b for b in bahasa_diminta if b not in tersedia]
        if dilewati:
            print(
                f"Catatan: bahasa {', '.join(dilewati)} belum terpasang di Stirling-PDF-mu, "
                f"OCR hanya memakai: {', '.join(bahasa_dipakai) or '(tidak ada)'}. Untuk memasang "
                "bahasa Indonesia: buka aplikasi Stirling-PDF > menu OCR > unduh paket bahasa "
                "'ind' (lihat docs/panduan-stirling-pdf.md)."
            )
        if not bahasa_dipakai:
            raise Gagal(
                f"Tidak satu pun bahasa yang diminta ({', '.join(bahasa_diminta)}) terpasang di "
                f"Stirling-PDF-mu. Bahasa yang tersedia sekarang: {', '.join(tersedia)}."
            )

    try:
        ctype, nama, isi = coba(bahasa_dipakai)
    except Gagal as e:
        if "language" in str(e).lower() and bahasa_dipakai != ["eng"]:
            print(
                "Catatan: bahasa yang diminta ditolak server, mencoba ulang dengan bahasa "
                "Inggris saja."
            )
            ctype, nama, isi = coba(["eng"])
        else:
            raise
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_tunggal(args.file, "-ocr")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil OCR (PDF sekarang bisa dicari/di-copy teksnya) -> {hasil.resolve()}")


def cmd_foto_ke_pdf(args):
    periksa_file_ada(*args.file)
    base = ambil_base_url(args.url)
    field_file = [("fileInput", f) for f in args.file]
    field_biasa = [
        ("fitOption", args.fit),
        ("colorType", args.warna),
        ("autoRotate", "true"),
    ]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/convert/img/pdf",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_banyak(
        args.file[0], f"{Path(args.file[0]).stem}.pdf")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil diubah jadi PDF ({len(args.file)} foto) -> {hasil.resolve()}")


def cmd_putar(args):
    periksa_file_ada(args.file)
    if args.derajat not in (90, 180, 270):
        raise Gagal("--derajat harus 90, 180, atau 270.")
    base = ambil_base_url(args.url)
    field_biasa = [("angle", str(args.derajat))]
    field_file = [("fileInput", args.file)]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/general/rotate-pdf",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_tunggal(args.file, f"-putar{args.derajat}")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil diputar {args.derajat} derajat -> {hasil.resolve()}")


def cmd_watermark(args):
    periksa_file_ada(args.file)
    base = ambil_base_url(args.url)
    field_biasa = [
        ("watermarkType", "text"),
        ("watermarkText", args.teks),
        ("alphabet", "roman"),
        ("fontSize", str(args.ukuran)),
        ("rotation", str(args.putaran)),
        ("opacity", str(args.opasitas)),
        ("widthSpacer", "50"),
        ("heightSpacer", "50"),
        ("customColor", args.warna),
        ("convertPDFToImage", "false"),
    ]
    field_file = [("fileInput", args.file)]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/security/add-watermark",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_tunggal(args.file, "-watermark")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil ditambah watermark '{args.teks}' -> {hasil.resolve()}")


def cmd_kunci(args):
    periksa_file_ada(args.file)
    if len(args.sandi) < 4:
        raise Gagal("Kata sandi minimal 4 karakter (disarankan lebih panjang & tidak mudah ditebak).")
    base = ambil_base_url(args.url)
    field_biasa = [
        ("password", args.sandi),
        ("ownerPassword", args.sandi_pemilik or ""),
        ("keyLength", str(args.panjang_kunci)),
        ("preventAssembly", "false"),
        ("preventExtractContent", "false"),
        ("preventExtractForAccessibility", "false"),
        ("preventFillInForm", "false"),
        ("preventModify", "false"),
        ("preventModifyAnnotations", "false"),
        ("preventPrinting", "false"),
        ("preventPrintingFaithful", "false"),
    ]
    field_file = [("fileInput", args.file)]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/security/add-password",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_tunggal(args.file, "-terkunci")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil dikunci kata sandi -> {hasil.resolve()}")
    print("PENTING: simpan kata sandi ini baik-baik. Tanpa itu, PDF tidak bisa dibuka lagi.")


def cmd_buka_kunci(args):
    periksa_file_ada(args.file)
    base = ambil_base_url(args.url)
    field_biasa = [("password", args.sandi)]
    field_file = [("fileInput", args.file)]
    ctype, nama, isi = panggil_stirling(base, ambil_api_key(args.api_key), "/api/v1/security/remove-password",
                                         field_biasa, field_file)
    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_tunggal(args.file, "-terbuka")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil dibuka kuncinya -> {hasil.resolve()}")


def cmd_rapikan_resi(args):
    periksa_file_ada(*args.file)
    if args.per_lembar not in (2, 4, 9, 16):
        raise Gagal("--per-lembar harus salah satu dari: 2, 4, 9, 16 (batasan Stirling-PDF).")
    base = ambil_base_url(args.url)
    api_key = ambil_api_key(args.api_key)

    if len(args.file) > 1:
        field_file = [("fileInput", f) for f in args.file]
        field_biasa = [("sortType", "orderProvided"), ("removeCertSign", "true"), ("generateToc", "false")]
        _ctype, _nama, gabungan = panggil_stirling(base, api_key, "/api/v1/general/merge-pdfs",
                                                    field_biasa, field_file)
        tmp = Path(args.file[0]).with_name("_tmp_gabungan_resi.pdf")
        tmp.write_bytes(gabungan)
        file_sumber = tmp
    else:
        file_sumber = Path(args.file[0])
        tmp = None

    try:
        field_biasa = [
            ("mode", "DEFAULT"),
            ("pagesPerSheet", str(args.per_lembar)),
            ("arrangement", "BY_ROWS"),
            ("readingDirection", "LTR"),
            ("orientation", args.orientasi),
            ("addBorder", "true" if args.garis_batas else "false"),
            ("borderWidth", "1"),
        ]
        field_file = [("fileInput", str(file_sumber))]
        ctype, nama, isi = panggil_stirling(base, api_key, "/api/v1/general/multi-page-layout",
                                             field_biasa, field_file)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)

    tujuan = Path(args.keluaran) if args.keluaran else keluaran_default_banyak(
        args.file[0], f"resi-rapi-{args.per_lembar}-per-lembar.pdf")
    hasil, _ = simpan_hasil(isi, ctype, nama, tujuan)
    print(f"Berhasil disusun {args.per_lembar} resi per lembar ({len(args.file)} file sumber) -> {hasil.resolve()}")
    print("Catatan: cek dulu di Print Preview sebelum cetak massal - Stirling-PDF menyusun ukuran")
    print("lembar otomatis berdasarkan ukuran halaman asli, bukan dipaksa persis A4/A6.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def tambah_argumen_umum(sub):
    sub.add_argument("--url", help="Alamat Stirling-PDF (default: ENV STIRLING_URL atau http://localhost:8080)")
    sub.add_argument("--api-key", help="API key Stirling-PDF bila keamanan diaktifkan (default: ENV STIRLING_API_KEY)")


def main():
    ap = argparse.ArgumentParser(prog="pdf.py", description=f"{APLIKASI} v{VERSI} - olah PDF via Stirling-PDF lokal")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p = sub.add_parser("cek", help="Cek Stirling-PDF hidup & lihat versinya")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_cek)

    p = sub.add_parser("gabung", help="Gabung beberapa PDF jadi satu")
    p.add_argument("file", nargs="+", help="File PDF yang digabung, urut sesuai urutan diketik")
    p.add_argument("--urutan", default="orderProvided",
                   choices=["orderProvided", "byFileName", "byDateModified", "byDateCreated", "byPDFTitle"])
    p.add_argument("--keluaran", help="Path file hasil (default: <file1>-gabungan.pdf)")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_gabung)

    p = sub.add_parser("pisah-halaman", help="Pisah PDF jadi satu file per halaman")
    p.add_argument("file")
    p.add_argument("--keluaran-folder", help="Folder hasil (default: <file>-per-halaman/)")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_pisah_halaman)

    p = sub.add_parser("pisah-rentang", help="Ambil rentang halaman tertentu jadi satu PDF baru")
    p.add_argument("file")
    p.add_argument("--halaman", required=True, help='Contoh: "3-7" atau "1,3,5-9"')
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_pisah_rentang)

    p = sub.add_parser("kompres", help="Perkecil ukuran PDF (untuk batas kirim WA/email/marketplace)")
    p.add_argument("file")
    p.add_argument("--level", type=int, default=4, help="1 (ringan) - 9 (maksimal), default 4")
    p.add_argument("--target", help='Ukuran target, mis. "500KB" atau "2MB" (opsional)')
    p.add_argument("--hitam-putih", action="store_true", help="Ubah jadi hitam-putih untuk ukuran lebih kecil")
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_kompres)

    p = sub.add_parser("ocr", help="Jadikan PDF hasil scan bisa dicari/di-copy teksnya (OCR)")
    p.add_argument("file")
    p.add_argument("--bahasa", nargs="+", default=None,
                   help="Kode bahasa Tesseract, default: ind eng (otomatis coba eng saja bila 'ind' belum terpasang)")
    p.add_argument("--tipe", default="skip-text", choices=["skip-text", "force-ocr", "Normal"],
                   help="skip-text = lewati halaman yang sudah ada teksnya (default, paling aman)")
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_ocr)

    p = sub.add_parser("foto-ke-pdf", help="Ubah satu/beberapa foto (nota, KTP, dll.) jadi satu PDF")
    p.add_argument("file", nargs="+")
    p.add_argument("--fit", default="maintainAspectRatio",
                   choices=["fillPage", "fitDocumentToImage", "maintainAspectRatio"])
    p.add_argument("--warna", default="color", choices=["color", "greyscale", "blackwhite"])
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_foto_ke_pdf)

    p = sub.add_parser("putar", help="Putar semua halaman PDF")
    p.add_argument("file")
    p.add_argument("--derajat", type=int, required=True, choices=[90, 180, 270])
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_putar)

    p = sub.add_parser("watermark", help="Tambah watermark teks (mis. DRAF, RAHASIA)")
    p.add_argument("file")
    p.add_argument("--teks", required=True)
    p.add_argument("--ukuran", type=float, default=30)
    p.add_argument("--opasitas", type=float, default=0.5, help="0.0 (transparan) - 1.0 (pekat)")
    p.add_argument("--putaran", type=float, default=45, help="Derajat kemiringan teks")
    p.add_argument("--warna", default="#d3d3d3", help="Kode warna hex, default abu-abu muda")
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_watermark)

    p = sub.add_parser("kunci", help="Kunci PDF dengan kata sandi")
    p.add_argument("file")
    p.add_argument("--sandi", required=True, help="Kata sandi untuk membuka file")
    p.add_argument("--sandi-pemilik", help="Kata sandi pemilik (opsional, batasi cetak/edit)")
    p.add_argument("--panjang-kunci", type=int, default=256, choices=[40, 128, 256])
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_kunci)

    p = sub.add_parser("buka-kunci", help="Buka kunci kata sandi PDF (perlu tahu kata sandinya)")
    p.add_argument("file")
    p.add_argument("--sandi", required=True)
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_buka_kunci)

    p = sub.add_parser("rapikan-resi", help="Susun beberapa resi marketplace jadi beberapa per lembar untuk dicetak hemat kertas")
    p.add_argument("file", nargs="+", help="Satu file PDF berisi banyak resi, atau beberapa file 1 resi per file")
    p.add_argument("--per-lembar", type=int, default=4, choices=[2, 4, 9, 16])
    p.add_argument("--orientasi", default="PORTRAIT", choices=["PORTRAIT", "LANDSCAPE"])
    p.add_argument("--garis-batas", action="store_true", help="Tambah garis tipis pemisah antar resi")
    p.add_argument("--keluaran", help="Path file hasil")
    tambah_argumen_umum(p)
    p.set_defaults(fungsi=cmd_rapikan_resi)

    args = ap.parse_args()
    try:
        args.fungsi(args)
    except Gagal as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
