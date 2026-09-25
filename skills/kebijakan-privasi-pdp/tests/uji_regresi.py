#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi scripts/cek_kebijakan.py (hanya library standar).

Jalankan dari mana saja:  python3 tests/uji_regresi.py   (Windows: python / py)
Keluar 0 bila semua lulus.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

SINI = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.dirname(SINI)
SCRIPT = os.path.join(AKAR, "scripts", "cek_kebijakan.py")
TEMPLATES = os.path.join(AKAR, "templates")

BAIK = """# Kebijakan Privasi Dapur Bu Sari
Berlaku sejak: 1 Oktober 2026. Terakhir diperbarui: 25 September 2026.

## 1. Siapa kami
Dapur Bu Sari (usaha perorangan milik Sari Wulandari, Jl. Melati No. 5, Bandung) adalah pengendali data pribadi untuk toko online dan akun WhatsApp Business kami. Kontak urusan data: privasi@dapurbusari.id atau WhatsApp 0812-0000-0000.

## 2. Data pribadi yang kami kumpulkan
Nama, nomor WhatsApp, alamat pengiriman, riwayat pesanan, dan bukti transfer.

## 3. Tujuan, dasar pemrosesan, dan masa simpan
Data digunakan untuk memproses dan mengirim pesanan (dasar pemrosesan: pelaksanaan perjanjian), menjawab pertanyaan pelanggan, dan mengirim promo bila Anda setuju (dasar: persetujuan). Catatan transaksi disimpan selama 10 tahun untuk kewajiban pembukuan pajak; chat tanpa transaksi disimpan paling lama 1 tahun lalu dihapus.

## 4. Pihak penerima
Kami tidak menjual data pribadi Anda. Data dibagikan seperlunya kepada kurir/ekspedisi dan payment gateway untuk mengirim dan memproses pembayaran.

## 5. Luar negeri
WhatsApp (Meta) dan Google Drive dapat menyimpan data di server di luar Indonesia. Kami memakai penyedia dengan pelindungan memadai sesuai UU PDP Pasal 56.

## 6. Hak Anda
Anda berhak mengakses dan meminta salinan data, memperbaiki data, menghapus data, dan menarik persetujuan kapan saja.

## 7. Cara mengajukan permintaan
Kirim permintaan ke email atau WhatsApp di atas. Kami menanggapi paling lambat 3×24 jam.

## 8. Keamanan
Akses data dibatasi hanya untuk pemilik dan satu admin, memakai kata sandi kuat dan verifikasi dua langkah.

## 9. Kebocoran data
Jika terjadi kegagalan pelindungan data pribadi, kami memberi tahu Anda dan lembaga berwenang secara tertulis paling lambat 3×24 jam.

## 10. Perubahan kebijakan
Perubahan kebijakan akan kami umumkan lewat WhatsApp paling lambat 7 hari sebelum berlaku.
"""

BURUK = """KEBIJAKAN PRIVASI
Dengan menggunakan website ini Anda dianggap telah menyetujui seluruh ketentuan.
Kami dapat menjual data pelanggan kepada mitra kami.
Kami tidak bertanggung jawab atas kebocoran data yang terjadi.
Kebijakan dapat diubah sewaktu-waktu tanpa pemberitahuan.
Data disimpan selamanya.
"""

EN_BURUK = """Privacy Policy. By using this site you agree to this policy. We may sell your personal information to partners.
We are not responsible for any data breach. You are deemed to have consented. This policy complies with GDPR.
"""

gagal = []
n_uji = 0


def jalan(args, kode=None):
    p = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, encoding="utf-8")
    if kode is not None and p.returncode != kode:
        raise AssertionError("kode {} (harap {}) untuk {}: {} {}".format(p.returncode, kode, args, p.stdout[-300:], p.stderr[-300:]))
    return p


def json_dari(path):
    p = jalan([path, "--format", "json"], 0)
    return json.loads(p.stdout)


def cek(nama, kondisi, info=""):
    global n_uji
    n_uji += 1
    if not kondisi:
        gagal.append("{} {}".format(nama, info))


def tulis(folder, nama, isi, mode="w", enc="utf-8"):
    path = os.path.join(folder, nama)
    if mode == "wb":
        with open(path, "wb") as f:
            f.write(isi)
    else:
        with open(path, "w", encoding=enc, newline="\n") as f:
            f.write(isi)
    return path


def unsur(r, uid):
    return next((u for u in r["unsur"] if u["id"] == uid), None)


def main():
    tmp = tempfile.mkdtemp(prefix="uji_pdp_")
    try:
        # 1. Kebijakan lengkap
        r = json_dari(tulis(tmp, "baik.md", BAIK))
        cek("baik: skor 100", r["skor"] == 100, r["skor"])
        cek("baik: status CUKUP LENGKAP", r["status"] == "CUKUP LENGKAP", r["status"])
        cek("baik: tidak ada risiko (negasi 'tidak menjual')", r["risiko"] == [], r["risiko"])
        cek("baik: tak ada isian kosong", r["isian_kosong"] == 0)

        # 2. Kebijakan buruk
        r = json_dari(tulis(tmp, "buruk.md", BURUK))
        tinggi = [x for x in r["risiko"] if x["tingkat"] == "TINGGI"]
        cek("buruk: status KURANG LENGKAP", r["status"] == "KURANG LENGKAP", r["status"])
        cek("buruk: >=4 frasa TINGGI", len(tinggi) >= 4, len(tinggi))
        teks_risiko = " ".join(x["kutipan"] for x in r["risiko"])
        for frasa in ("dianggap", "menjual", "bertanggung jawab", "selamanya", "tanpa pemberitahuan"):
            cek("buruk: terdeteksi '{}'".format(frasa), frasa in teks_risiko.lower(), teks_risiko)
        cek("buruk: catatan teks pendek", any("pendek" in c for c in r["catatan"]))
        cek("buruk: 'diubah tanpa pemberitahuan' bukan unsur perubahan", unsur(r, "perubahan")["status"] == "TIDAK ADA")
        cek("buruk: 'tidak bertanggung jawab atas kebocoran' bukan unsur kebocoran", unsur(r, "kebocoran")["status"] == "TIDAK ADA")
        cek("buruk: browse-wrap tidak ganda dengan 'dianggap'",
            len([x for x in r["risiko"] if x["baris"] == 2]) == 1, r["risiko"])
        cek("buruk: nomor baris benar", any(x["baris"] == 3 for x in r["risiko"]), r["risiko"])

        # 3. Bahasa Inggris berisiko + negasi EN
        r = json_dari(tulis(tmp, "en.md", EN_BURUK))
        lv = [(x["tingkat"], x["kutipan"]) for x in r["risiko"]]
        cek("en: sell terdeteksi", any("sell" in k.lower() and t == "TINGGI" for t, k in lv), lv)
        cek("en: deemed terdeteksi", any("deemed" in k.lower() for t, k in lv), lv)
        cek("en: gdpr terdeteksi", any("gdpr" in k.lower() for t, k in lv), lv)
        r = json_dari(tulis(tmp, "en_ok.md", "We do not sell your personal data. We never sell your information.\n"))
        cek("en: negasi tidak ditandai", not any("sell" in x["kutipan"].lower() for x in r["risiko"]), r["risiko"])

        # 4. Unsur bersyarat: data spesifik & anak
        r = json_dari(tulis(tmp, "klinik.md", "Klinik kami mencatat keluhan pasien dan riwayat alergi. Anak di bawah umur juga dilayani.\n"))
        cek("klinik: data_spesifik muncul & TIDAK ADA", (unsur(r, "data_spesifik") or {}).get("status") == "TIDAK ADA")
        cek("klinik: data_anak muncul & TIDAK ADA", (unsur(r, "data_anak") or {}).get("status") == "TIDAK ADA")
        r = json_dari(tulis(tmp, "umum.md", BAIK))
        cek("umum: data_anak tidak diwajibkan", unsur(r, "data_anak") is None)

        # 5. Hak subjek sebagian
        r = json_dari(tulis(tmp, "hak.md", "Anda dapat mengakses data dan meminta penghapusan data.\n"))
        h = unsur(r, "hak_subjek")
        cek("hak: SEBAGIAN", h["status"] == "SEBAGIAN", h)
        cek("hak: kurang koreksi & tarik", set(h["kurang"]) == {"koreksi", "tarik_persetujuan"}, h["kurang"])
        cek("hak: nilai 1.0 dari 2", abs(h["nilai"] - 1.0) < 1e-9, h["nilai"])

        # 6. Saran transfer LN bila menyebut layanan asing
        r = json_dari(tulis(tmp, "ln.md", "Kami menyimpan data pesanan di Google Sheets.\n"))
        cek("ln: catatan transfer", any("Pasal 56" in c for c in r["catatan"]), r["catatan"])

        # 7. Encoding: cp1252, UTF-8 BOM, UTF-16
        r = json_dari(tulis(tmp, "cp.txt", BAIK.replace("Bu Sari", "Café Sari").encode("cp1252", errors="replace"), mode="wb"))
        cek("cp1252: terbaca & skor 100", r["skor"] == 100, r["skor"])
        r = json_dari(tulis(tmp, "bom.md", b"\xef\xbb\xbf" + BAIK.encode("utf-8"), mode="wb"))
        cek("utf-8 BOM: skor 100", r["skor"] == 100, r["skor"])
        r = json_dari(tulis(tmp, "u16.txt", BAIK.encode("utf-16"), mode="wb"))
        cek("utf-16: skor 100", r["skor"] == 100, r["skor"])

        # 8. Input buruk: tanpa traceback, exit 2
        kasus = {
            "kosong": tulis(tmp, "kosong.md", ""),
            "spasi": tulis(tmp, "spasi.md", "   \n\n\t "),
            "docx": tulis(tmp, "x.docx", b"PK\x03\x04isi", mode="wb"),
            "pdf": tulis(tmp, "x.pdf", b"%PDF-1.7 isi", mode="wb"),
            "biner": tulis(tmp, "x.bin", b"\x00\x01\x02abc\x00", mode="wb"),
            "folder": tmp,
            "hilang": os.path.join(tmp, "tidak-ada.md"),
        }
        for nama, path in kasus.items():
            p = jalan([path], 2)
            cek("input {}: GALAT tanpa traceback".format(nama),
                "GALAT" in p.stderr and "Traceback" not in p.stderr + p.stdout, p.stderr)
            pj = jalan([path, "--format", "json"], 2)
            cek("input {}: json galat".format(nama), "galat" in json.loads(pj.stdout))
        p = jalan([], 2)
        cek("tanpa argumen: GALAT", "GALAT" in p.stderr and "Traceback" not in p.stderr)

        # 9. Mode lain
        p = jalan(["--daftar"], 0)
        cek("--daftar", "Unsur yang diperiksa" in p.stdout)
        jalan([os.path.join(tmp, "buruk.md"), "--ketat"], 1)
        jalan([os.path.join(tmp, "baik.md"), "--ketat"], 0)
        p = jalan([os.path.join(tmp, "buruk.md")], 0)
        cek("teks: memuat bagian", "FRASA BERISIKO" in p.stdout and "YANG PERLU DITAMBAHKAN" in p.stdout)

        # 10. Template bawaan: unsur lengkap, status PERLU DILENGKAPI karena [isi: ...]
        for nama in ("kebijakan-privasi.md", "kebijakan-privasi-en.md"):
            r = json_dari(os.path.join(TEMPLATES, nama))
            cek("template {}: skor >= 95".format(nama), r["skor"] >= 95, r["skor"])
            cek("template {}: tanpa risiko".format(nama), r["risiko"] == [], r["risiko"])
            cek("template {}: PERLU DILENGKAPI".format(nama), r["status"] == "PERLU DILENGKAPI", r["status"])
    except AssertionError as e:
        gagal.append(str(e))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if gagal:
        print("GAGAL {} dari {} uji:".format(len(gagal), n_uji))
        for g in gagal:
            print(" - " + g)
        return 1
    print("LULUS: {} uji".format(n_uji))
    return 0


if __name__ == "__main__":
    sys.exit(main())
