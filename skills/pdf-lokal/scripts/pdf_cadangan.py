#!/usr/bin/env python3
"""pdf-lokal (Komunitech) - JALUR CADANGAN tanpa Stirling-PDF.

Dipakai bila Stirling-PDF belum terpasang/menyala. Script ini TIDAK memasang apa pun.
Ia hanya memakai alat PDF yang SUDAH ada di komputer pengguna:
  - qpdf                       (gabung, pisah, putar, kunci, buka-kunci, kompres ringan)
  - Ghostscript (gs / gswin64c) (kompres sungguhan, cadangan gabung & pisah-rentang)
  - pdftk                      (gabung, pisah, putar, kunci, buka-kunci)
Semua alat dipanggil langsung sebagai daftar argumen (tanpa shell), file asli tidak
pernah ditimpa, dan tidak ada yang dikirim ke internet. Hanya library standar Python 3.8+.

Contoh:
  python3 pdf_cadangan.py alat
  python3 pdf_cadangan.py gabung nota-a.pdf nota-b.pdf nota-c.pdf --keluaran nota-gabungan.pdf
  python3 pdf_cadangan.py kompres nota-gabungan.pdf --level sedang
  python3 pdf_cadangan.py pisah-rentang laporan.pdf --halaman 3-7
  python3 pdf_cadangan.py pisah-halaman kontrak.pdf
  python3 pdf_cadangan.py putar scan.pdf --derajat 90
  python3 pdf_cadangan.py kunci slip-gaji.pdf --sandi Rahasia123
  python3 pdf_cadangan.py buka-kunci slip-gaji-terkunci.pdf --sandi Rahasia123
Paksa alat tertentu: --alat qpdf|gs|pdftk (default: pilih otomatis yang tersedia).
"""
import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VERSI = "1.0.5"
APLIKASI = "pdf-lokal (cadangan)"

# Perintah yang didukung per alat, urutan = prioritas pemilihan otomatis.
DUKUNGAN = {
    "gabung": ["qpdf", "pdftk", "gs"],
    "pisah-rentang": ["qpdf", "pdftk", "gs"],
    "pisah-halaman": ["qpdf", "pdftk"],
    "putar": ["qpdf", "pdftk"],
    "kunci": ["qpdf", "pdftk"],
    "buka-kunci": ["qpdf", "pdftk"],
    "kompres": ["gs", "qpdf"],  # gs mengecilkan gambar; qpdf hanya optimasi tanpa-rugi
}
TIDAK_DIDUKUNG = {
    "ocr": "OCR butuh Stirling-PDF (atau aplikasi OCR lain yang sudah terpasang)",
    "watermark": "watermark butuh Stirling-PDF",
    "foto-ke-pdf": "foto ke PDF butuh Stirling-PDF; cadangan manual: buka foto lalu Cetak > 'Microsoft Print to PDF' (Windows) / Preview > Ekspor sebagai PDF (macOS)",
    "rapikan-resi": "menyusun beberapa resi per lembar butuh Stirling-PDF; cadangan manual: di dialog Cetak pilih 'Halaman per lembar: 2 atau 4'",
}
GS_PRESET = {"ringan": "/printer", "sedang": "/ebook", "kuat": "/screen"}


class Gagal(Exception):
    """Error yang pesannya aman & jelas untuk ditampilkan ke pengguna awam."""


# ---------------------------------------------------------------------------
# Deteksi alat
# ---------------------------------------------------------------------------

def cari_alat(env_path=None):
    """Kembalikan dict nama_alat -> path executable (hanya yang ditemukan di PATH)."""
    ditemukan = {}
    calon = {
        "qpdf": ["qpdf"],
        "gs": ["gs", "gswin64c", "gswin32c"],
        "pdftk": ["pdftk"],
    }
    for nama, daftar in calon.items():
        for exe in daftar:
            p = shutil.which(exe, path=env_path)
            if p:
                ditemukan[nama] = p
                break
    return ditemukan


def pilih_alat(perintah, tersedia, paksa=None):
    urutan = DUKUNGAN[perintah]
    if paksa:
        if paksa not in urutan:
            raise Gagal(f"Alat '{paksa}' tidak dipakai untuk '{perintah}' di skill ini. Pilihan: {', '.join(urutan)}.")
        if paksa not in tersedia:
            raise Gagal(f"Alat '{paksa}' tidak ditemukan di komputer ini.")
        return paksa
    for nama in urutan:
        if nama in tersedia:
            return nama
    raise Gagal(
        f"Tidak ada alat PDF lokal untuk '{perintah}' di komputer ini (dicari: {', '.join(urutan)}). "
        "Skill ini TIDAK memasang apa pun sendiri. Pilihan: (1) nyalakan/pasang Stirling-PDF - lihat "
        "references/pasang-stirling.md; (2) minta pengguna memasang salah satu alat itu sendiri "
        "(lihat bagian 'Jalur cadangan' di SKILL.md); (3) cara manual di SKILL.md."
    )


# ---------------------------------------------------------------------------
# Utilitas file
# ---------------------------------------------------------------------------

def path_keluaran_aman(diinginkan):
    p = Path(diinginkan)
    if not p.exists():
        return p
    n = 1
    while True:
        kandidat = p.with_name(f"{p.stem}({n}){p.suffix}")
        if not kandidat.exists():
            return kandidat
        n += 1


def keluaran(args, akhiran, file_asli=None):
    asli = Path(file_asli or (args.file[0] if isinstance(args.file, list) else args.file))
    if getattr(args, "keluaran", None):
        tujuan = Path(args.keluaran)
        if tujuan.resolve() in {Path(f).resolve() for f in _semua_file(args)}:
            raise Gagal("Path keluaran sama dengan file asli. File asli tidak boleh ditimpa; pilih nama lain.")
        return path_keluaran_aman(tujuan)
    return path_keluaran_aman(asli.with_name(f"{asli.stem}{akhiran}.pdf"))


def _semua_file(args):
    return args.file if isinstance(args.file, list) else [args.file]


def periksa_input(args):
    hilang = [f for f in _semua_file(args) if not Path(f).is_file()]
    if hilang:
        raise Gagal("File tidak ditemukan: " + ", ".join(hilang))
    bukan_pdf = []
    for f in _semua_file(args):
        with open(f, "rb") as fh:
            if b"%PDF" not in fh.read(1024):
                bukan_pdf.append(f)
    if bukan_pdf:
        raise Gagal("Bukan file PDF (atau rusak): " + ", ".join(bukan_pdf) +
                    ". Untuk foto/gambar, lihat bagian foto-ke-pdf di SKILL.md.")


def pastikan_pdf_jadi(path):
    p = Path(path)
    if not p.is_file() or p.stat().st_size == 0:
        raise Gagal("Alat selesai tetapi file hasil tidak terbentuk. File asli tidak berubah.")
    with open(p, "rb") as fh:
        if not fh.read(8).startswith(b"%PDF"):
            p.unlink(missing_ok=True)
            raise Gagal("File hasil bukan PDF yang valid, sudah dihapus. File asli tidak berubah.")


def kb(n):
    return f"{n / 1024:.0f} KB"


def parse_rentang(teks):
    """'3-7' / '1,3,5-9' -> list[(awal, akhir)]. Validasi ketat, tanpa 'z'/'end'."""
    if not re.fullmatch(r"\s*\d+(\s*-\s*\d+)?(\s*,\s*\d+(\s*-\s*\d+)?)*\s*", teks or ""):
        raise Gagal('Format halaman tidak dikenali. Contoh yang benar: "3-7" atau "1,3,5-9".')
    hasil = []
    for bagian in teks.replace(" ", "").split(","):
        if "-" in bagian:
            a, b = (int(x) for x in bagian.split("-"))
        else:
            a = b = int(bagian)
        if a < 1 or b < a:
            raise Gagal(f"Rentang halaman '{bagian}' tidak valid (halaman mulai dari 1, awal <= akhir).")
        hasil.append((a, b))
    return hasil


# ---------------------------------------------------------------------------
# Menjalankan alat (tanpa shell)
# ---------------------------------------------------------------------------

def jalankan(cmd, sukses=(0,)):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        raise Gagal("Proses terlalu lama (lebih dari 10 menit) dan dihentikan. Coba file yang lebih kecil.") from None
    except OSError as e:
        raise Gagal(f"Alat tidak bisa dijalankan: {e}") from None
    if r.returncode not in sukses:
        pesan = (r.stderr or r.stdout or "").strip().splitlines()
        pesan = " | ".join(pesan[-3:])[:400]
        if re.search(r"password|encrypt|OWNER PASSWORD|invalid password", pesan, re.IGNORECASE):
            raise Gagal("PDF ini terkunci kata sandi, atau kata sandinya salah. Periksa ejaan/besar-kecil "
                        "huruf, atau buka dulu dengan perintah 'buka-kunci --sandi ...'.")
        if re.search(r"out of range|beyond|exceeds|page.*not exist", pesan, re.IGNORECASE):
            raise Gagal("Nomor halaman melebihi jumlah halaman file. Cek jumlah halamannya dulu, lalu ulangi "
                        f"dengan rentang yang benar. (Detail: {pesan[:200]})")
        raise Gagal(f"Alat gagal memproses file (kode {r.returncode}): {pesan or '(tanpa pesan)'}. "
                    "Pastikan file bisa dibuka normal di pembaca PDF.")
    return r


QPDF_OK = (0, 3)  # qpdf: 3 = selesai dengan peringatan (hasil tetap valid)


def qpdf_argfile(exe, argumen):
    """Jalankan qpdf dengan argumen dari file sementara (@file) supaya kata sandi tidak
    terlihat di daftar proses. File sementara dibuat privat lalu langsung dihapus."""
    fd, nama = tempfile.mkstemp(prefix="pdf-lokal-", suffix=".args")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("\n".join(argumen) + "\n")
        return jalankan([exe, f"@{nama}"], QPDF_OK)
    finally:
        try:
            os.unlink(nama)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Perintah
# ---------------------------------------------------------------------------

def cmd_alat(args, tersedia):
    print(f"Pemeriksaan alat PDF lokal ({platform.system()} {platform.release()}, Python {platform.python_version()}):")
    for nama in ("qpdf", "gs", "pdftk"):
        print(f"  {nama:6}: {'ADA  -> ' + tersedia[nama] if nama in tersedia else 'tidak ada'}")
    print("Perintah yang bisa dijalankan lewat jalur cadangan:")
    ada_satu = False
    for perintah, urutan in DUKUNGAN.items():
        pakai = next((a for a in urutan if a in tersedia), None)
        if pakai:
            ada_satu = True
            catatan = " (hanya optimasi tanpa-rugi; gambar tidak dikecilkan)" if perintah == "kompres" and pakai == "qpdf" else ""
            print(f"  BISA  {perintah:14} via {pakai}{catatan}")
        else:
            print(f"  TIDAK {perintah:14} (butuh salah satu: {', '.join(urutan)})")
    for perintah, alasan in TIDAK_DIDUKUNG.items():
        print(f"  TIDAK {perintah:14} ({alasan})")
    if not ada_satu:
        print("KESIMPULAN: tidak ada alat PDF lokal. Jangan memasang apa pun tanpa izin pengguna; "
              "tawarkan references/pasang-stirling.md atau cara manual di SKILL.md.")
    else:
        print("KESIMPULAN: jalur cadangan siap untuk perintah bertanda BISA.")


def cmd_gabung(args, tersedia):
    periksa_input(args)
    if len(args.file) < 2:
        raise Gagal("Butuh minimal 2 file PDF untuk digabung.")
    alat = pilih_alat("gabung", tersedia, args.alat)
    tujuan = keluaran(args, "-gabungan")
    exe = tersedia[alat]
    if alat == "qpdf":
        jalankan([exe, "--empty", "--pages", *args.file, "--", str(tujuan)], QPDF_OK)
    elif alat == "pdftk":
        jalankan([exe, *args.file, "cat", "output", str(tujuan)])
    else:
        jalankan([exe, "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dQUIET", "-sDEVICE=pdfwrite",
                  f"-sOutputFile={tujuan}", *args.file])
    pastikan_pdf_jadi(tujuan)
    print(f"Berhasil digabung ({len(args.file)} file, urut: {', '.join(Path(f).name for f in args.file)}) via {alat}")
    print(f"  -> {tujuan.resolve()}")


def cmd_pisah_rentang(args, tersedia):
    periksa_input(args)
    rentang = parse_rentang(args.halaman)
    alat = pilih_alat("pisah-rentang", tersedia, args.alat)
    if alat == "gs" and len(rentang) > 1:
        raise Gagal("Ghostscript hanya bisa satu rentang (mis. 3-7). Pakai qpdf/pdftk untuk rentang ganda.")
    teks = ",".join(f"{a}-{b}" if a != b else str(a) for a, b in rentang)
    tujuan = keluaran(args, f"-hal-{teks.replace(',', '_')}")
    exe = tersedia[alat]
    if alat == "qpdf":
        jalankan([exe, args.file, "--pages", ".", teks, "--", str(tujuan)], QPDF_OK)
    elif alat == "pdftk":
        jalankan([exe, args.file, "cat", *[f"{a}-{b}" if a != b else str(a) for a, b in rentang], "output", str(tujuan)])
    else:
        a, b = rentang[0]
        jalankan([exe, "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dQUIET", "-sDEVICE=pdfwrite",
                  f"-dFirstPage={a}", f"-dLastPage={b}", f"-sOutputFile={tujuan}", args.file])
    pastikan_pdf_jadi(tujuan)
    print(f"Berhasil mengambil halaman {teks} via {alat}")
    print(f"  -> {tujuan.resolve()}")


def cmd_pisah_halaman(args, tersedia):
    periksa_input(args)
    alat = pilih_alat("pisah-halaman", tersedia, args.alat)
    asli = Path(args.file)
    folder = path_keluaran_aman(Path(args.keluaran_folder) if args.keluaran_folder
                                else asli.with_name(f"{asli.stem}-per-halaman"))
    folder.mkdir(parents=True)
    exe = tersedia[alat]
    if alat == "qpdf":
        jalankan([exe, "--split-pages", str(asli), str(folder / "halaman-%d.pdf")], QPDF_OK)
    else:
        jalankan([exe, str(asli), "burst", "output", str(folder / "halaman-%02d.pdf")])
        (folder / "doc_data.txt").unlink(missing_ok=True)  # file metadata bawaan pdftk
    daftar = sorted(folder.glob("*.pdf"))
    if not daftar:
        raise Gagal("Tidak ada halaman yang terbentuk. File asli tidak berubah.")
    print(f"Berhasil dipisah jadi {len(daftar)} file via {alat}")
    print(f"  -> folder {folder.resolve()}")
    for p in daftar:
        print(f"     {p.name}")


def cmd_putar(args, tersedia):
    periksa_input(args)
    alat = pilih_alat("putar", tersedia, args.alat)
    tujuan = keluaran(args, f"-putar{args.derajat}")
    exe = tersedia[alat]
    if alat == "qpdf":
        jalankan([exe, args.file, str(tujuan), f"--rotate=+{args.derajat}"], QPDF_OK)
    else:
        arah = {90: "east", 180: "south", 270: "west"}[args.derajat]
        jalankan([exe, args.file, "cat", f"1-end{arah}", "output", str(tujuan)])
    pastikan_pdf_jadi(tujuan)
    print(f"Berhasil diputar {args.derajat} derajat (searah jarum jam, semua halaman) via {alat}")
    print(f"  -> {tujuan.resolve()}")


def cmd_kunci(args, tersedia):
    periksa_input(args)
    if len(args.sandi) < 4:
        raise Gagal("Kata sandi minimal 4 karakter (disarankan lebih panjang & tidak mudah ditebak).")
    alat = pilih_alat("kunci", tersedia, args.alat)
    tujuan = keluaran(args, "-terkunci")
    exe = tersedia[alat]
    if alat == "qpdf":
        pemilik = args.sandi_pemilik or args.sandi
        qpdf_argfile(exe, [args.file, str(tujuan), "--encrypt", args.sandi, pemilik, "256", "--"])
        enkripsi = "AES-256"
    else:
        cmd = [exe, args.file, "output", str(tujuan), "user_pw", args.sandi, "encrypt_aes128"]
        if args.sandi_pemilik:
            cmd[4:4] = ["owner_pw", args.sandi_pemilik]
        jalankan(cmd)
        enkripsi = "AES-128"
    pastikan_pdf_jadi(tujuan)
    print(f"Berhasil dikunci kata sandi ({enkripsi}) via {alat}")
    print(f"  -> {tujuan.resolve()}")
    print("PENTING: simpan kata sandi ini baik-baik. Tanpa itu, PDF tidak bisa dibuka lagi.")
    print("Saran: kirim kata sandi lewat jalur berbeda dari file-nya (mis. file via WA, sandi via telepon/SMS).")


def cmd_buka_kunci(args, tersedia):
    periksa_input(args)
    alat = pilih_alat("buka-kunci", tersedia, args.alat)
    tujuan = keluaran(args, "-terbuka")
    exe = tersedia[alat]
    if alat == "qpdf":
        qpdf_argfile(exe, [f"--password={args.sandi}", "--decrypt", args.file, str(tujuan)])
    else:
        jalankan([exe, args.file, "input_pw", args.sandi, "output", str(tujuan)])
    pastikan_pdf_jadi(tujuan)
    print(f"Berhasil dibuka kuncinya via {alat}")
    print(f"  -> {tujuan.resolve()}")


def cmd_kompres(args, tersedia):
    periksa_input(args)
    alat = pilih_alat("kompres", tersedia, args.alat)
    tujuan = keluaran(args, "-kompres")
    exe = tersedia[alat]
    if alat == "gs":
        jalankan([exe, "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dQUIET", "-sDEVICE=pdfwrite",
                  "-dCompatibilityLevel=1.5", f"-dPDFSETTINGS={GS_PRESET[args.level]}",
                  "-dDetectDuplicateImages=true", f"-sOutputFile={tujuan}", args.file])
    else:
        jalankan([exe, args.file, str(tujuan), "--object-streams=generate", "--compress-streams=y",
                  "--recompress-flate", "--compression-level=9"], QPDF_OK)
    pastikan_pdf_jadi(tujuan)
    awal, akhir = Path(args.file).stat().st_size, tujuan.stat().st_size
    if akhir >= awal:
        tujuan.unlink()
        print(f"Tidak bisa dikecilkan lagi via {alat} (asli {kb(awal)}, hasil {kb(akhir)}). "
              "File hasil dibuang; pakai file asli." +
              ("" if args.level == "kuat" or alat != "gs" else " Bisa coba --level kuat (kualitas gambar turun)."))
        return
    turun = round((awal - akhir) * 100 / awal)
    print(f"Berhasil dikompres via {alat} (level {args.level}): {kb(awal)} -> {kb(akhir)} (turun {turun}%)")
    print(f"  -> {tujuan.resolve()}")
    if alat == "qpdf":
        print("Catatan: qpdf hanya optimasi tanpa-rugi; PDF hasil scan/foto biasanya baru mengecil banyak lewat Ghostscript.")
    if akhir > 100 * 1024 * 1024:
        print("PERINGATAN: masih di atas 100 MB (batas dokumen WhatsApp). Coba --level kuat atau pisah file.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(prog="pdf_cadangan.py",
                                 description=f"{APLIKASI} v{VERSI} - olah PDF dengan qpdf/Ghostscript/pdftk yang sudah terpasang")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p = sub.add_parser("alat", help="Cek alat PDF lokal yang tersedia & perintah yang bisa dipakai")
    p.set_defaults(fungsi=cmd_alat)

    def umum(p):
        p.add_argument("--alat", choices=["qpdf", "gs", "pdftk"], help="Paksa alat tertentu (default otomatis)")

    p = sub.add_parser("gabung", help="Gabung beberapa PDF jadi satu, urut sesuai diketik")
    p.add_argument("file", nargs="+")
    p.add_argument("--keluaran")
    umum(p)
    p.set_defaults(fungsi=cmd_gabung)

    p = sub.add_parser("pisah-rentang", help="Ambil rentang halaman jadi satu PDF baru")
    p.add_argument("file")
    p.add_argument("--halaman", required=True, help='Contoh: "3-7" atau "1,3,5-9"')
    p.add_argument("--keluaran")
    umum(p)
    p.set_defaults(fungsi=cmd_pisah_rentang)

    p = sub.add_parser("pisah-halaman", help="Pisah PDF jadi satu file per halaman")
    p.add_argument("file")
    p.add_argument("--keluaran-folder")
    umum(p)
    p.set_defaults(fungsi=cmd_pisah_halaman)

    p = sub.add_parser("putar", help="Putar semua halaman (searah jarum jam)")
    p.add_argument("file")
    p.add_argument("--derajat", type=int, required=True, choices=[90, 180, 270])
    p.add_argument("--keluaran")
    umum(p)
    p.set_defaults(fungsi=cmd_putar)

    p = sub.add_parser("kunci", help="Kunci PDF dengan kata sandi")
    p.add_argument("file")
    p.add_argument("--sandi", required=True)
    p.add_argument("--sandi-pemilik")
    p.add_argument("--keluaran")
    umum(p)
    p.set_defaults(fungsi=cmd_kunci)

    p = sub.add_parser("buka-kunci", help="Buka kunci kata sandi (perlu tahu sandinya)")
    p.add_argument("file")
    p.add_argument("--sandi", required=True)
    p.add_argument("--keluaran")
    umum(p)
    p.set_defaults(fungsi=cmd_buka_kunci)

    p = sub.add_parser("kompres", help="Perkecil ukuran PDF (WA/email/marketplace)")
    p.add_argument("file")
    p.add_argument("--level", default="sedang", choices=list(GS_PRESET))
    p.add_argument("--keluaran")
    umum(p)
    p.set_defaults(fungsi=cmd_kompres)

    args = ap.parse_args(argv)
    try:
        args.fungsi(args, cari_alat())
    except Gagal as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
