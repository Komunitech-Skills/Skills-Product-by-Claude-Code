#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi perjanjian.py (hanya library standar).

Jalankan: python3 uji_regresi.py  -> keluar 0 bila semua lulus.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(SINI, "perjanjian.py")
TEMPLATES = os.path.join(os.path.dirname(SINI), "templates")

# Draf berisiko dari penguji independen (harus RUJUK PROFESIONAL)
DRAF_RISIKO = {
    "investasi": """# PERJANJIAN INVESTASI USAHA KOPI
Para pihak sepakat PIHAK PERTAMA menanamkan dana investasi Rp 50.000.000 (lima puluh juta rupiah) dan menerima keuntungan 5% per bulan.
## Pasal 1
Ruang lingkup
""",
    "kavling": """# PERJANJIAN PENGIKATAN JUAL BELI KAVLING
PIHAK PERTAMA menjual sebidang kavling SHM No. 123 seluas 120 m2 seharga Rp 150.000.000 (seratus lima puluh juta rupiah).
## Pasal 1
""",
    "pinjam_bpkb": """# PERJANJIAN PINJAM UANG
PIHAK KEDUA meminjam Rp 20.000.000 (dua puluh juta rupiah) dengan bunga 3% per bulan dan menyerahkan BPKB motor sebagai jaminan.
## Pasal 1
""",
    "harga_minimum": """# RESELLER
PIHAK KEDUA wajib menjual dengan harga tidak kurang dari harga minimum Rp 50.000 (lima puluh ribu rupiah), pelanggaran dikenakan denda Rp 5.000.000 (lima juta ribu rupiah).
## Pasal 1
## Pasal 3
""",
    "banting_harga": """# RESELLER
PIHAK KEDUA dilarang menjual di bawah Rp 25.000 per botol dan dilarang banting harga.
## Pasal 1
""",
    "tanah_besar": """# JUAL BELI
Jual beli tanah seluas 200 m2 senilai Rp 750.000.000 (tujuh ratus lima puluh juta rupiah).
## Pasal 1
""",
}
KATA_RUJUK = {"investasi": "investasi", "kavling": "PPAT", "pinjam_bpkb": "jaminan", "harga_minimum": "UU 5/1999",
              "banting_harga": "UU 5/1999", "tanah_besar": "PPAT"}


def jalan(args, kode=0):
    p = subprocess.run([sys.executable, SCRIPT, "--format", "json"] + args, capture_output=True, text=True,
                       encoding="utf-8")
    if p.returncode != kode:
        raise AssertionError("kode {} (harap {}) untuk {}: {}".format(p.returncode, kode, args, p.stderr))
    return json.loads(p.stdout) if kode == 0 else None


def cek(nama, kondisi, info=""):
    if not kondisi:
        raise AssertionError("GAGAL: {} {}".format(nama, info))
    print("  ok  " + nama)


def main():
    tmp = tempfile.mkdtemp(prefix="uji-perjanjian-")
    try:
        # --- deteksi risiko
        for nama, isi in DRAF_RISIKO.items():
            f = os.path.join(tmp, nama + ".md")
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(isi)
            d = jalan(["cek", f])
            cek("rujuk: " + nama, d["status"] == "RUJUK PROFESIONAL" and
                any(KATA_RUJUK[nama] in r for r in d["rujuk_profesional"]), d["rujuk_profesional"])
        d = jalan(["cek", os.path.join(tmp, "harga_minimum.md")])
        cek("terbilang salah terdeteksi", any("tidak cocok" in m for m in d["masalah"]))
        cek("penomoran loncat terdeteksi", any("tidak urut" in m for m in d["masalah"]))
        # --- template bersih tidak memicu rujukan palsu
        for n in sorted(os.listdir(TEMPLATES)):
            d = jalan(["cek", os.path.join(TEMPLATES, n)])
            cek("template tanpa rujukan palsu: " + n, not d["rujuk_profesional"], d["rujuk_profesional"])
        # catatan TINJAU PENGACARA yang menyebut harga minimum tidak memicu rujukan
        f = os.path.join(tmp, "catatan.md")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("# X\n## Pasal 1\nHarga jual yang disarankan Rp 25.000 (dua puluh lima ribu rupiah).\n"
                     "> ⚠ TINJAU PENGACARA: Anda meminta harga minimum dan larangan banting harga.\n")
        cek("catatan TINJAU tidak dihitung", not jalan(["cek", f])["rujuk_profesional"])

        # --- angka
        cek("terbilang 1.001.000", jalan(["terbilang", "1.001.000"])["terbilang"] == "satu juta seribu rupiah")
        cek("terbilang 111.111", jalan(["terbilang", "111111"])["terbilang"] ==
            "seratus sebelas ribu seratus sebelas rupiah")
        cek("peringatan '2,5' tanpa satuan", jalan(["terbilang", "2,5"])["catatan"])
        cek("tanpa peringatan '2,5jt'", not jalan(["terbilang", "2,5jt"])["catatan"])
        t = jalan(["termin", "--total", "10.000.001", "--persen", "33,33,34"])
        cek("termin total tepat", sum(x["nilai"] for x in t["termin"]) == 10000001)
        cek("sampai +12 bulan", jalan(["sampai", "2026-10-01", "--bulan", "12"])["berakhir"] == "2027-09-30")
        cek("sampai 31 Jan +1 bulan", jalan(["sampai", "2026-01-31", "--bulan", "1"])["berakhir"] == "2026-02-28")
        cek("sampai +30 hari", jalan(["sampai", "2026-10-01", "--hari", "30"])["berakhir"] == "2026-10-30")
        r = jalan(["retainer", "--per-bulan", "3jt", "--bulan", "6", "--mulai", "2026-10-01"])
        cek("retainer total", r["total"] == 18000000 and len(r["jadwal"]) == 6)
        cek("retainer jatuh tempo", r["jadwal"][1]["jatuh_tempo"] == "5 November 2026")
        cek("meterai kuitansi default 1", jalan(["meterai", "--jenis", "kwitansi", "--nilai", "6jt"])["jumlah_meterai"] == 1)
        cek("meterai perjanjian default 2", jalan(["meterai"])["jumlah_meterai"] == 2)
        cek("kuitansi 5jt tidak wajib", not jalan(["meterai", "--jenis", "kwitansi", "--nilai", "5.000.000"])["wajib"])
        d = jalan(["denda", "--nilai", "5jt", "--persen-per-hari", "0,1", "--hari", "30", "--maks-persen", "5"])
        cek("denda 150.000", d["denda"] == 150000)
        # --- input rusak
        jalan(["termin", "--total", "1000", "--persen", "30,30"], kode=1)
        jalan(["terbilang", "abc"], kode=1)
        jalan(["terbilang", "5m"], kode=1)
        jalan(["sampai", "2026-10-01"], kode=1)
        jalan(["retainer", "--per-bulan", "1jt", "--bulan", "2", "--mulai", "2026-01-31"], kode=1)
        kosong = os.path.join(tmp, "kosong.md")
        open(kosong, "w").close()
        jalan(["cek", kosong], kode=1)
        print("SEMUA UJI LULUS")
        return 0
    except AssertionError as e:
        print(e)
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
