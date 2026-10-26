#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi perjanjian.py (hanya library standar).

Jalankan: python3 uji_regresi.py  -> keluar 0 bila semua lulus.
"""
import json
import re
import os
import shutil
import subprocess
import sys
import tempfile

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(SINI, "perjanjian.py")
SKILL_DIR = os.path.dirname(SINI)
TEMPLATES = os.path.join(SKILL_DIR, "templates")
VERSI_HARAP = "1.0.9"
KALIMAT_BERKAS = "Draf juga sudah saya simpan sebagai berkas. Balas 'kirim file' bila mau dikirim sebagai dokumen."

# Balasan bot gelombang pra-cek 2026-10-21 (dipendekkan): harus PERLU PERBAIKAN
BALASAN_BURUK = {
    "jalur berkas": "Draf juga saya simpan di file: `/opt/ochome/.openclaw/workspace/draft_sewa_kios.md`",
    "nama berkas": "Sudah saya simpan sebagai draft_sewa_kios_sri_mulyani.md ya.",
    "istilah script": "(saya hitung pakai script biar angka & terbilangnya akurat)",
    "istilah skrip": "Angka sudah dicek skrip, aman.",
    "istilah exec/tool": "Saya jalankan exec dan tool pemeriksa dulu.",
    "blok kode": "Bagian 1/2\n```\nPERJANJIAN SEWA\n```",
    "judul markdown": "Bagian 1/2\n# PERJANJIAN SEWA-MENYEWA TEMPAT USAHA\n## Pasal 1",
    "tabel pipa": "LAMPIRAN 1\n| No | Bagian | Kondisi |\n|---|---|---|\n| 1 | Pintu | baik |",
    "isian lama": "NIK: [[NIK PIHAK PERTAMA]]",
    "terlalu panjang": "PASAL 1\n" + "Kalimat isi pasal yang panjang sekali. " * 360,
}
BALASAN_BAIK = ("Bagian 1/1\n\nPERJANJIAN SEWA\nPASAL 1 — OBJEK\n(1) Denda 0,1%/hari, Rp 9.000/hari, ditanggung dan/atau "
                "dibayar penyewa. Kondisi baik/rusak ringan.\nNIK: [isi: NIK]\n\nAngka & terbilang sudah dihitung ulang.\n"
                + KALIMAT_BERKAS)

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


def tulis(folder, nama, isi):
    f = os.path.join(folder, nama)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(isi)
    return f


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
        # v1.0.4: tanggal tanda tangan tidak diisi otomatis; [isi: ...] terdeteksi sebagai isian kosong
        d = jalan(["tanggal"])
        cek("tanggal tanpa argumen -> [isi: tanggal], bukan hari ini",
            d["tanggal"] is None and "[isi: tanggal]" in d["kalimat_pembuka"], d)
        d = jalan(["tanggal", "2026-10-05"])
        cek("tanggal diberikan -> Senin 5 Oktober 2026", d["hari"] == "Senin" and d["tanggal"] == "2026-10-05")
        fi = os.path.join(tmp, "isi.md")
        with open(fi, "w", encoding="utf-8") as f:
            f.write("# PERJANJIAN SEWA\nPada hari ini, [isi: hari], tanggal [isi: tanggal] ...\n## Pasal 1\n")
        d = jalan(["cek", fi])
        cek("cek menandai [isi: tanggal] sebagai isian kosong", "[isi: tanggal]" in json.dumps(d, ensure_ascii=False), d)
        # v1.0.5: konsistensi beban biaya (satu pihak per pos, tidak bertentangan antar pasal/asumsi)
        dasar = ("# PERJANJIAN SEWA KIOS\n## Pasal 4\n### Hak dan Kewajiban PIHAK PERTAMA\n(2) PIHAK PERTAMA wajib:\n"
                 "   a. menanggung perbaikan besar yang bukan akibat kesalahan PIHAK KEDUA;\n"
                 "## Pasal 5\n### Hak dan Kewajiban PIHAK KEDUA\n(2) PIHAK KEDUA wajib:\n"
                 "   b. membayar listrik, air, dan iuran pengelola pasar selama masa sewa;\n"
                 "### Asumsi dari template\n")
        kasus = {
            "konflik": (dasar + "- PBB/iuran pengelola pasar ditanggung pemilik (Pasal 4).\n", True),
            "konsisten": (dasar + "- Iuran pengelola pasar ditanggung penyewa (Pasal 5).\n", False),
            "masing2": (dasar + "- Biaya keamanan ditanggung masing-masing PIHAK PERTAMA dan PIHAK KEDUA.\n", False),
            "listrik_dua": (dasar + "(3) Biaya listrik dibayar oleh PIHAK PERTAMA.\n", True),
        }
        for nama, (isi, harap) in kasus.items():
            fk = os.path.join(tmp, "beban_" + nama + ".md")
            with open(fk, "w", encoding="utf-8") as fh:
                fh.write(isi)
            d = jalan(["cek", fk])
            ada = any("bertentangan" in m for m in d["masalah"])
            cek("beban biaya {}: konflik={}".format(nama, harap), ada == harap, d["masalah"])
        d = jalan(["cek", os.path.join(tmp, "beban_konflik.md")])
        cek("konflik menyebut iuran pasar", any("iuran/retribusi pasar" in m for m in d["masalah"]), d["masalah"])
        cek("perbaikan besar ke PIHAK PERTAMA (bukan pihak yang disebut di anak kalimat)",
            d["beban_biaya"].get("perbaikan besar") == ["PIHAK PERTAMA"], d["beban_biaya"])
        d = jalan(["cek", os.path.join(TEMPLATES, "sewa-tempat.md")])
        cek("template sewa-tempat konsisten", not any("bertentangan" in m for m in d["masalah"]) and
            d["beban_biaya"].get("PBB") == ["PIHAK PERTAMA"] and d["beban_biaya"].get("listrik") == ["PIHAK KEDUA"],
            d["beban_biaya"])
        for n in sorted(os.listdir(TEMPLATES)):
            d = jalan(["cek", os.path.join(TEMPLATES, n)])
            cek("template tanpa konflik beban: " + n, not any("bertentangan" in m for m in d["masalah"]), d["masalah"])
        # v1.0.6: pengosongan sepihak bukan default; tanpa peringatan -> harus diperbaiki, dengan peringatan -> info
        kasus = {
            "sepihak_polos": ("# SEWA KIOS\n## Pasal 7\n(3) PIHAK PERTAMA berhak mengunci kios dan mengeluarkan barang "
                              "PIHAK KEDUA tanpa proses hukum.\n", "masalah"),
            "sepihak_diminta": ("# SEWA KIOS\n## Pasal 7\n(3) PIHAK KEDUA menyetujui PIHAK PERTAMA mengunci Objek Sewa.\n"
                                "> ⚠ TINJAU PENGACARA: risiko perbuatan melawan hukum.\n", "info"),
            "aman": ("# SEWA KIOS\n## Pasal 7\n(4) PIHAK PERTAMA tidak akan mengunci, menyegel, atau mengambil alih "
                     "Objek Sewa tanpa persetujuan PIHAK KEDUA atau putusan pengadilan.\n", None),
        }
        for nama, (isi, tempat) in kasus.items():
            fk = os.path.join(tmp, nama + ".md")
            with open(fk, "w", encoding="utf-8") as fh:
                fh.write(isi)
            d = jalan(["cek", fk])
            di_m = any("sepihak" in m for m in d["masalah"])
            di_i = any("sepihak" in m for m in d["info"])
            cek("pengosongan " + nama, (di_m, di_i) == (tempat == "masalah", tempat == "info"), d)
        for n in sorted(os.listdir(TEMPLATES)):
            d = jalan(["cek", os.path.join(TEMPLATES, n)])
            cek("template tanpa pengosongan sepihak default: " + n,
                not any("sepihak" in m for m in d["masalah"] + d["info"]), d["masalah"] + d["info"])
        # --- v1.0.9: versi
        p = subprocess.run([sys.executable, SCRIPT, "--versi"], capture_output=True, text=True, encoding="utf-8")
        cek("versi script " + VERSI_HARAP, p.returncode == 0 and VERSI_HARAP in p.stdout, p.stdout + p.stderr)
        with open(os.path.join(SKILL_DIR, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        cek("versi README " + VERSI_HARAP, "Versi terkini: **{}**".format(VERSI_HARAP) in readme)
        with open(os.path.join(SKILL_DIR, "CHANGELOG.md"), encoding="utf-8") as fh:
            cek("versi CHANGELOG " + VERSI_HARAP, "revisi {} ".format(VERSI_HARAP) in fh.read())
        # --- v1.0.9: satu gaya isian [isi: ...] di SKILL.md, templates, references, contoh 01-05
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as fh:
            skill = fh.read()
        cek("SKILL.md < 300 baris", len(skill.splitlines()) < 300)
        cek("SKILL.md kalimat berkas tanpa jalur", KALIMAT_BERKAS in skill)
        cek("SKILL.md aturan < 3.800 karakter & teks biasa", "3.800" in skill and "BUKAN di dalam blok kode" in skill)
        cek("SKILL.md larangan kata script/skrip/tool/exec", "script, skrip, tool, exec" in skill)
        sisa = []
        for folder in ("templates", "references", "examples"):
            for n in sorted(os.listdir(os.path.join(SKILL_DIR, folder))):
                if folder == "examples" and not n[:2] in ("01", "02", "03", "04", "05"):
                    continue  # 00-* & HASIL-UJI = rekaman uji lama, dibiarkan apa adanya
                with open(os.path.join(SKILL_DIR, folder, n), encoding="utf-8") as fh:
                    isi = re.sub(r"`\[\[\.\.\.\]\]`", "", fh.read())  # penyebutan aturan, bukan isian
                if re.search(r"\[\[[^\]]+\]\]", isi):
                    sisa.append(folder + "/" + n)
        skill_isian = re.sub(r"`\[\[\.\.\.\]\]`", "", skill)
        if re.search(r"\[\[[^\]]+\]\]", skill_isian):
            sisa.append("SKILL.md")
        cek("satu gaya isian [isi: ...]", not sisa, sisa)
        # --- v1.0.9: bagi -> teks biasa, Bagian i/N, < 3.800 karakter, potong antar-pasal
        for n in sorted(os.listdir(TEMPLATES)):
            f = os.path.join(TEMPLATES, n)
            with open(f, encoding="utf-8") as fh:
                asli = fh.read()
            d = jalan(["bagi", f])
            bag = d["bagian"]
            gabung = "\n".join(bag)
            nm = d["jumlah_bagian"]
            cek("bagi {}: tiap bagian <= 3800".format(n), all(len(b) <= 3800 for b in bag), d["panjang"])
            cek("bagi {}: label Bagian i/{}".format(n, nm),
                all(b.startswith("Bagian {}/{}\n".format(i + 1, nm)) for i, b in enumerate(bag)))
            cek("bagi {}: potong hanya antar-pasal".format(n),
                all(re.match(r"(?i)(pasal \d+|lampiran|demikian)", b.split("\n", 2)[2]) for b in bag[1:]),
                [b.split("\n", 2)[2][:40] for b in bag[1:]])
            pasal_asli = len(re.findall(r"(?im)^#+\s*pasal\s+\d+", asli))
            pasal_baru = len(re.findall(r"(?m)^PASAL \d+", gabung))
            cek("bagi {}: jumlah pasal utuh ({})".format(n, pasal_asli), pasal_asli == pasal_baru, pasal_baru)
            for ayat in re.findall(r"(?m)^\(\d+\) .{20,60}", asli):
                if "**" not in ayat and "[[" not in ayat:
                    if ayat not in gabung:
                        raise AssertionError("GAGAL: bagi {} kehilangan ayat: {}".format(n, ayat))
            cek("bagi {}: nominal/meterai tetap".format(n),
                re.findall(r"Rp ?[\d.]+", re.sub(r"<!--[\s\S]*?-->", "", asli)) == re.findall(r"Rp ?[\d.]+", gabung))
            b = jalan(["cek-balasan", tulis(tmp, "balas-" + n, ("\n\n<<<PESAN BERIKUTNYA>>>\n\n").join(bag))])
            cek("bagi {}: lolos cek-balasan".format(n), b["status"] == "SIAP KIRIM", b["masalah"])
        # pasal sangat panjang -> dipotong di batas ayat, tetap <= maks
        panjang = "# PERJANJIAN UJI\n\n## Pasal 1\n### Isi\n" + "".join(
            "({}) {}\n".format(i, "Ketentuan ayat yang cukup panjang untuk uji. " * 8) for i in range(1, 30)) + \
            "\n## Pasal 2\n### Penutup\n(1) Selesai.\n"
        d = jalan(["bagi", tulis(tmp, "panjang.md", panjang)])
        cek("bagi pasal > maks: dipotong di ayat + catatan", all(len(b) <= 3800 for b in d["bagian"]) and d["catatan"]
            and all(re.match(r"\(\d+\)|PASAL", b.split("\n", 2)[2]) for b in d["bagian"][1:]), d["panjang"])
        d = jalan(["bagi", "--maks", "2000", os.path.join(TEMPLATES, "sewa-tempat.md")])
        cek("bagi --maks 2000", all(len(b) <= 2000 for b in d["bagian"]) and d["jumlah_bagian"] >= 4, d["panjang"])
        jalan(["bagi", "--maks", "100", os.path.join(TEMPLATES, "sewa-tempat.md")], kode=1)
        cek("bagi --maks terlalu kecil ditolak", True)
        # tabel tanda tangan & lampiran -> baris pendek, isian lama diseragamkan
        d = jalan(["bagi", tulis(tmp, "lama.md", "# PERJANJIAN\n## Pasal 1\nNIK: [[NIK]]\n\n| PIHAK PERTAMA | PIHAK KEDUA |\n"
                                                  "|---|---|\n| <br>[Meterai Rp10.000]<br> | <br>[Meterai Rp10.000]<br> |\n"
                                                  "| **[[NAMA A]]** | **[[NAMA B]]** |\n\n### Lampiran 1\n| No | Bagian | Kondisi |\n"
                                                  "|---|---|---|\n| 1 | Pintu | baik |\n")])
        t = "\n".join(d["bagian"])
        cek("bagi: tanpa [[ ]], |, #, **", not re.search(r"\[\[|\||^#|\*\*", t, re.M), t)
        cek("bagi: tanda tangan per pihak", "PIHAK PERTAMA\n[Meterai Rp10.000]\n[isi: NAMA A]" in t, t)
        cek("bagi: lampiran baris pendek", "1. Bagian: Pintu; Kondisi: baik" in t, t)
        d = jalan(["cek", tulis(tmp, "lama2.md", "# P\n## Pasal 1\nNIK [[NIK]]\n")])
        cek("cek: info gaya isian [[...]]", any("[isi: ...]" in x for x in d["info"]), d["info"])
        # --- v1.0.9: cek-balasan
        for nama, isi in BALASAN_BURUK.items():
            d = jalan(["cek-balasan", tulis(tmp, "buruk.txt", isi)])
            cek("cek-balasan menolak: " + nama, d["status"] == "PERLU PERBAIKAN", d)
        d = jalan(["cek-balasan", tulis(tmp, "baik.txt", BALASAN_BAIK)])
        cek("cek-balasan menerima balasan bersih (dan/atau, Rp/hari, baik/rusak)", d["status"] == "SIAP KIRIM", d["masalah"])
        d = jalan(["cek-balasan", tulis(tmp, "dua.txt", "Bagian 1/2\n" + "a " * 1800 + "\nBagian 2/2\n" + "b " * 1800)])
        cek("cek-balasan: hitung per Bagian", d["status"] == "SIAP KIRIM" and d["jumlah_pesan"] == 2, d)
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
