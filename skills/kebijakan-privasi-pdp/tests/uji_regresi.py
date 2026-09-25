#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi scripts/cek_kebijakan.py v1.0.1 (hanya library standar).

Termasuk tes untuk tiap temuan HASIL-UJI (T-1, T-2, S-1..S-5, R-1..R-4) dan tabel akurasi
dari set kalimat berlabel (tests/data/kalimat-berlabel.json).

Jalankan dari mana saja:  python3 tests/uji_regresi.py   (Windows: python / py)
Keluar 0 bila semua lulus.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

SINI = os.path.dirname(os.path.abspath(__file__))
AKAR = os.path.dirname(SINI)
SCRIPT = os.path.join(AKAR, "scripts", "cek_kebijakan.py")
TEMPLATES = os.path.join(AKAR, "templates")
DATA = os.path.join(SINI, "data")
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import cek_kebijakan as ck  # noqa: E402

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


def risiko(teks):
    return ck.periksa(teks)["risiko"]


def status_unsur(teks, uid):
    r = ck.periksa(teks + "\n" + "isi " * 200)
    u = unsur(r, uid)
    return u["status"] if u else None


def uji_akurasi():
    """Tabel akurasi: set kalimat berlabel dari HASIL-UJI (§2b 45 frasa, §2c 13 unsur) + set kontrol."""
    with open(os.path.join(DATA, "kalimat-berlabel.json"), encoding="utf-8") as f:
        d = json.load(f)
    tabel = []
    for kunci_f, kunci_u, target_f, target_u in (("frasa_hasil_uji", "unsur_hasil_uji", 40, 11), ("frasa_tambahan", "unsur_tambahan", None, None)):
        benar = fp = fn = 0
        for k in d[kunci_f]:
            dapat = bool(risiko(k["kalimat"]))
            if dapat == k["berisiko"]:
                benar += 1
            elif dapat:
                fp += 1
                print("   salah-positif:", k["kalimat"])
            else:
                fn += 1
                print("   salah-negatif:", k["kalimat"])
        nf = len(d[kunci_f])
        bu = 0
        for k in d[kunci_u]:
            g = status_unsur(k["kalimat"], k["unsur"])
            if g == k["status"]:
                bu += 1
            else:
                print("   unsur salah: {} harap {} dapat {} | {}".format(k["unsur"], k["status"], g, k["kalimat"]))
        nu = len(d[kunci_u])
        tabel.append((kunci_f, benar, nf, fp, fn, bu, nu))
        if target_f:
            cek("akurasi frasa HASIL-UJI >= {}/{}".format(target_f, nf), benar >= target_f, "{}/{}".format(benar, nf))
            cek("akurasi unsur HASIL-UJI >= {}/{}".format(target_u, nu), bu >= target_u, "{}/{}".format(bu, nu))
        else:
            cek("akurasi set kontrol frasa >= 90%", benar >= 0.9 * nf, "{}/{}".format(benar, nf))
            cek("akurasi set kontrol unsur >= 80%", bu >= 0.8 * nu, "{}/{}".format(bu, nu))
    print("TABEL AKURASI (v{}):".format(ck.VERSI))
    print("  | Set | Frasa benar | Salah-positif | Salah-negatif | Unsur benar |")
    for nama, b, n, fp, fn, bu, nu in tabel:
        print("  | {} | {}/{} | {} | {} | {}/{} |".format(nama.replace("frasa_", ""), b, n, fp, fn, bu, nu))


def uji_v101(tmp):
    """Tes regresi untuk tiap temuan HASIL-UJI v1.0.0."""
    # T-1: kalimat patuh "tidak akan dijual" tidak boleh berisiko
    for k in ("Data Anda tidak akan dijual.", "Data Anda tidak dapat dijual kepada siapa pun.",
              "Informasi Anda tidak kami jual kepada siapa pun.", "Kami bukan perusahaan yang dapat menjual data Anda."):
        cek("T-1 bersih: " + k, risiko(k) == [], risiko(k))
    r = ck.periksa(BAIK.replace("Kami tidak menjual data pribadi Anda.", "Data Anda tidak akan dijual kepada siapa pun."))
    cek("T-1: kebijakan baik + 'tidak akan dijual' tetap CUKUP LENGKAP", r["status"] == "CUKUP LENGKAP", (r["status"], r["risiko"]))

    # T-2: "tidak akan memberi tahu bila bocor" = TINGGI dan unsur kebocoran TIDAK terpenuhi
    k = "Kami tidak akan memberi tahu Anda bila terjadi kebocoran data."
    rr = risiko(k)
    cek("T-2: frasa TINGGI", any(x["tingkat"] == "TINGGI" for x in rr), rr)
    cek("T-2: unsur kebocoran TIDAK ADA", status_unsur(k, "kebocoran") == "TIDAK ADA")
    r = ck.periksa(BAIK.replace("kami memberi tahu Anda dan lembaga berwenang", "kami tidak akan memberi tahu Anda maupun lembaga berwenang"))
    cek("T-2: kebijakan baik yang diubah jadi 'tidak akan memberi tahu' turun status",
        unsur(r, "kebocoran")["status"] == "TIDAK ADA" and r["status"] == "PERLU PERBAIKAN", (unsur(r, "kebocoran"), r["status"]))
    cek("T-2: polaritas umum — 'tidak mengakses data' bukan hak akses",
        "akses" in unsur(ck.periksa("Anda tidak dapat mengakses data Anda. " + "isi " * 200), "hak_subjek")["kurang"])
    cek("T-2: negasi ganda 'tidak ... tanpa memberi tahu' = unsur perubahan ADA",
        status_unsur("Kami tidak akan mengubah kebijakan ini tanpa memberi tahu Anda terlebih dahulu.", "perubahan") == "ADA")

    # S-1: variasi jual/sewa/bagikan untuk imbalan (ID & EN)
    for k in ("We may sell or rent your personal information.", "We may share and sell your data to partners.",
              "We may disclose your information to advertisers for payment.", "We reserve the right to sell, rent or lease customer data.",
              "Kami berhak memperdagangkan data pelanggan.", "Kami dapat memonetisasi data Anda.",
              "Kami dapat mengalihkan data pelanggan kepada mitra dengan imbalan.", "Kami dapat menukar database pelanggan dengan mitra.",
              "Data pelanggan dapat diperjualbelikan kepada mitra.", "Kami dapat menyewakan informasi kontak Anda kepada pengiklan."):
        rr = risiko(k)
        cek("S-1 terdeteksi TINGGI: " + k, any(x["tingkat"] == "TINGGI" for x in rr), rr)
    rr = risiko("We may share your information with third parties for their marketing purposes.")
    cek("S-1: share ke pihak ketiga untuk pemasaran mereka = SEDANG", [x["tingkat"] for x in rr] == ["SEDANG"], rr)
    cek("S-1: dengan persetujuan tidak ditandai", risiko("With your consent, we may share your information with partners for their marketing purposes.") == [])
    cek("S-1: alasan frasa EN berbahasa Indonesia (R-7)", "dilarang" in risiko("We may sell your data.")[0]["alasan"])
    cek("S-1: 'menjual produk' bukan jual data", risiko("Kami menjual produk fashion secara online dan melindungi data Anda.") == [])

    # S-2: isian kosong menurunkan skor & status
    r = ck.periksa(BAIK.replace("privasi@dapurbusari.id", "[isi: email]"))
    cek("S-2: satu isian → BELUM SIAP", r["status"] == "BELUM SIAP", r["status"])
    cek("S-2: satu isian → skor <= 84", r["skor"] <= 84, r["skor"])
    cek("S-2: skor struktur tetap 100", r["skor_struktur"] == 100, r["skor_struktur"])
    p = jalan([tulis(tmp, "isian.md", BAIK.replace("Bandung", "[isi: kota]"))], 0)
    cek("S-2: header teks menyebut isian kosong", "isian kosong dilengkapi" in p.stdout and "BELUM SIAP" in p.stdout, p.stdout[:300])
    r = ck.periksa("Kebijakan Privasi [isi: nama]\n[isi: data]\n[isi: tujuan]\n")
    cek("S-2: dokumen hanya isian → bukan CUKUP LENGKAP", r["status"] != "CUKUP LENGKAP" and r["skor"] < 50, (r["status"], r["skor"]))

    # S-3: pola unsur dengan kalimat nyata dari examples 01–03 (tests/data/contoh*.md)
    r = ck.periksa(open(os.path.join(DATA, "contoh01-toko-fashion-id.md"), encoding="utf-8").read())
    cek("S-3 contoh01: transfer LN (server Singapura) ADA", unsur(r, "transfer_ln")["status"] == "ADA")
    cek("S-3 contoh01: tanpa frasa berisiko", r["risiko"] == [], r["risiko"])
    cek("S-3 contoh01: struktur 100 & BELUM SIAP", r["skor_struktur"] == 100 and r["status"] == "BELUM SIAP", (r["skor_struktur"], r["status"]))
    cek("S-3 contoh01: skor 84 (dibatasi isian)", r["skor"] == 84, r["skor"])
    r = ck.periksa(open(os.path.join(DATA, "contoh01-toko-fashion-en.md"), encoding="utf-8").read())
    cek("S-3 contoh01 EN: struktur 100, tanpa risiko", r["skor_struktur"] == 100 and r["risiko"] == [], (r["skor_struktur"], r["risiko"]))
    r = ck.periksa(open(os.path.join(DATA, "contoh02-klinik-gform.md"), encoding="utf-8").read())
    cek("S-3 contoh02: identitas klinik terdeteksi", unsur(r, "identitas")["status"] == "ADA", unsur(r, "identitas"))
    cek("S-3 contoh02: jenis data terdeteksi", unsur(r, "jenis_data")["status"] == "ADA", unsur(r, "jenis_data"))
    cek("S-3 contoh02: 'di bawah 18 tahun' memicu data anak (ADA wali)", (unsur(r, "data_anak") or {}).get("status") == "ADA")
    cek("S-3 contoh02: masa simpan '[isi: 30] hari' = BELUM DIISI", unsur(r, "masa_simpan")["status"] == "BELUM DIISI", unsur(r, "masa_simpan"))
    r = ck.periksa(open(os.path.join(DATA, "contoh03-salinan-luar.md"), encoding="utf-8").read())
    tinggi = [x for x in r["risiko"] if x["tingkat"] == "TINGGI"]
    cek("S-3 contoh03: 3 frasa TINGGI", len(tinggi) == 3, [x["kutipan"] for x in tinggi])
    cek("S-3 contoh03: 'Hubungi kami di ...' bukan cara mengajukan", unsur(r, "cara_ajukan")["status"] == "TIDAK ADA")
    cek("S-3 contoh03: skor 41 (6,5 dari 16)", r["skor"] == 41, r["skor"])
    cek("S-3 contoh03: KURANG LENGKAP", r["status"] == "KURANG LENGKAP", r["status"])
    for k, uid, harap in (("Kami menyimpan data Anda selama 2 tahun.", "masa_simpan", "ADA"),
                          ("Data kami simpan 2 tahun sejak transaksi terakhir.", "masa_simpan", "ADA"),
                          ("Server kami berada di Singapura.", "transfer_ln", "ADA"),
                          ("Data disimpan di server Amerika Serikat milik Google.", "transfer_ln", "ADA"),
                          ("Kebijakan ini berlaku untuk Toko Kue Mawar.", "identitas", "ADA"),
                          ("Toko Kue Mawar adalah usaha milik Ibu Rina.", "identitas", "ADA"),
                          ("Hubungi kami di 0812-1111-2222.", "cara_ajukan", "TIDAK ADA"),
                          ("Kami menggunakan HTTPS dan membatasi akses admin.", "keamanan", "ADA"),
                          ("Seluruh data kami simpan di Indonesia dan tidak kami kirim ke luar negeri.", "transfer_ln", "ADA")):
        cek("S-3 unsur {}: {}".format(uid, k), status_unsur(k, uid) == harap, status_unsur(k, uid))
    h = unsur(ck.periksa("Anda dapat mencabut persetujuan kapan saja. " + "isi " * 200), "hak_subjek")
    cek("S-3: 'mencabut persetujuan' = tarik persetujuan", "tarik_persetujuan" not in h["kurang"], h)

    # S-5: "tidak ada sistem yang 100% aman" bukan frasa berisiko; klaim mutlak tetap ditandai
    cek("S-5: negasi 100% aman bersih", risiko("Tidak ada sistem yang 100% aman, tetapi kami membatasi akses.") == [])
    cek("S-5: 'No method is 100% secure' bersih", risiko("No method of transmission over the internet is 100% secure.") == [])
    cek("S-5: klaim mutlak tetap SEDANG", [x["tingkat"] for x in risiko("Data Anda 100% aman bersama kami.")] == ["SEDANG"])

    # R-2: HTML mentah (tag & entitas dibuang, nomor baris dipertahankan)
    htm = ("<html><head><style>p{}</style><script>var a='kami dapat menjual data';</script></head><body>\n"
           "<p>Kami <b>dapat</b> menjual data Anda.</p>\n<p>Kami dapat&nbsp;menyewakan data Anda.</p>\n"
           "<p>Data Anda tidak akan dijual.</p></body></html>\n")
    r = json_dari(tulis(tmp, "k.html", htm))
    cek("R-2: <b>dapat</b> & &nbsp; terdeteksi", sorted(x["baris"] for x in r["risiko"]) == [2, 3], r["risiko"])
    cek("R-2: isi <script> tidak diperiksa", all(x["baris"] != 1 for x in r["risiko"]))
    cek("R-2: kutipan tanpa tag", all("<" not in x["kutipan"] for x in r["risiko"]), r["risiko"])
    r1 = ck.periksa(BAIK)
    r2 = ck.periksa("<!DOCTYPE html><html><body>" + "".join("<p>{}</p>".format(b) for b in BAIK.splitlines() if b) + "</body></html>")
    cek("R-2: HTML minified = skor & jumlah kata sama", (r1["skor"], r1["risiko"]) == (r2["skor"], r2["risiko"]) and abs(r1["jumlah_kata"] - r2["jumlah_kata"]) <= 3,
        (r1["skor"], r2["skor"], r1["jumlah_kata"], r2["jumlah_kata"]))

    # R-3: UTF-16 tanpa BOM (LE & BE) terbaca
    for enc in ("utf-16-le", "utf-16-be"):
        r = json_dari(tulis(tmp, enc + ".txt", BAIK.encode(enc), mode="wb"))
        cek("R-3: {} tanpa BOM skor 100".format(enc), r["skor"] == 100, r["skor"])

    # R-1: kinerja linier & daftar temuan dibatasi
    buruk = "Kami dapat menjual data pelanggan kepada mitra. Data disimpan selamanya. Kami tidak bertanggung jawab atas kebocoran data.\n"
    kecil = tulis(tmp, "kecil.md", buruk * (500000 // len(buruk)))
    besar = tulis(tmp, "besar.md", buruk * (2000000 // len(buruk)))
    t0 = time.time(); jalan([kecil, "--format", "json"], 0); t1 = time.time()
    p = jalan([besar, "--format", "json"], 0); t2 = time.time()
    rb = json.loads(p.stdout)
    cek("R-1: 2 MB berisi banyak frasa berisiko < 6 detik (target ±2 dtk)", t2 - t1 < 6, "{:.2f}s".format(t2 - t1))
    cek("R-1: waktu linier (2 MB / 0,5 MB < 6x)", (t2 - t1) / max(0.05, t1 - t0) < 6, "{:.2f}s vs {:.2f}s".format(t1 - t0, t2 - t1))
    cek("R-1: daftar risiko dibatasi", len(rb["risiko"]) <= ck.MAKS_TEMUAN_TOTAL and any("hanya" in c for c in rb["catatan"]), len(rb["risiko"]))
    print("   kinerja: 0,5 MB {:.2f} dtk · 2 MB {:.2f} dtk".format(t1 - t0, t2 - t1))
    raksasa = os.path.join(tmp, "raksasa.md")
    with open(raksasa, "wb") as f:
        f.write(b"a" * (ck.BATAS_BYTE + 10))
    p = jalan([raksasa], 2)
    cek("R-1: file > 5 MB ditolak ramah", "terlalu besar" in p.stderr and "Traceback" not in p.stderr, p.stderr)

    # R-4: rujukan pasal di script
    idt = next(u for u in ck.UNSUR if u["id"] == "identitas")["dasar"]
    kon = next(u for u in ck.UNSUR if u["id"] == "kontak")["dasar"]
    cek("R-4: identitas tidak lagi merujuk Pasal 31", "31" not in idt and "Pasal 5" in idt, idt)
    cek("R-4: kontak tidak lagi 'Pasal 46 ayat (2) (narahubung)'", "46 ayat (2)" not in kon and "belum diverifikasi" in kon, kon)

    # S-4: template klinik tidak menjadikan persetujuan syarat pelayanan; ada varian Google Form tanpa tanda tangan
    with open(os.path.join(TEMPLATES, "pemberitahuan-persetujuan.md"), encoding="utf-8") as f:
        tp = f.read()
    bag_d = tp[tp.index("## D."):tp.index("## E.")]
    cek("S-4: tidak ada '(wajib untuk pelayanan)'", "wajib untuk pelayanan" not in bag_d.lower())
    cek("S-4: dasar pelaksanaan perjanjian & kewajiban hukum disebut", "pelaksanaan perjanjian" in bag_d and "kewajiban hukum" in bag_d)
    cek("S-4: persetujuan boleh ditolak tanpa kehilangan pelayanan", "pelayanan tetap diberikan" in bag_d)
    cek("S-4: ada varian D-online tanpa tanda tangan", "## D-online" in bag_d and "tanda tangan:" not in bag_d[bag_d.index("## D-online"):].lower())
    r = ck.periksa(tp)
    cek("S-4: template persetujuan tanpa frasa berisiko", r["risiko"] == [], r["risiko"])

    uji_akurasi()


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

        # 10. Template bawaan (S-2): isian kosong → tidak pernah 100, status BELUM SIAP, skor struktur 100
        for nama in ("kebijakan-privasi.md", "kebijakan-privasi-en.md"):
            r = json_dari(os.path.join(TEMPLATES, nama))
            cek("template {}: skor < 85 (isian kosong)".format(nama), r["skor"] <= 84, r["skor"])
            cek("template {}: skor struktur 100".format(nama), r["skor_struktur"] == 100, r["skor_struktur"])
            cek("template {}: tanpa risiko".format(nama), r["risiko"] == [], r["risiko"])
            cek("template {}: BELUM SIAP".format(nama), r["status"] == "BELUM SIAP", r["status"])
            cek("template {}: ada unsur BELUM DIISI".format(nama), any(u["status"] == "BELUM DIISI" for u in r["unsur"]))

        uji_v101(tmp)
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
