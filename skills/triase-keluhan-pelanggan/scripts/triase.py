#!/usr/bin/env python3
"""Pra-pilah keluhan pelanggan dari CSV (ekspor chat/ulasan): kategori, prioritas P1-P3, penanda eskalasi.

Pemakaian:
  python3 scripts/triase.py keluhan.csv                      (Windows: python / py)
  python3 scripts/triase.py keluhan.csv --nilai-besar 750000 --format ringkas

Hanya Python standar. Tidak membuka jaringan, tidak menulis file, tidak mengubah file masukan.
Hasil adalah DUGAAN berbasis kata kunci; agent wajib membaca ulang pesan aslinya.
Nomor HP, email, dan angka panjang di cuplikan disamarkan agar aman masuk rekap.
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation

MAKS_BARIS = 2000
NILAI_BESAR_DEFAULT = Decimal("500000")

# Nama kolom yang dikenali (huruf kecil, spasi/garis bawah disamakan)
ALIAS = {
    "pesan": ["pesan", "isi", "keluhan", "komentar", "ulasan", "review", "chat", "text", "teks", "isi_pesan", "catatan"],
    "bintang": ["bintang", "rating", "star", "stars", "skor"],
    "nilai": ["nilai", "total", "harga", "amount", "nominal", "nilai_pesanan", "total_pesanan"],
    "platform": ["platform", "kanal", "sumber", "channel", "toko"],
    "id": ["id", "no", "no_pesanan", "pesanan", "order", "order_id", "nomor_pesanan", "kode"],
    "menunggu": ["hari_menunggu", "menunggu", "umur", "usia", "hari", "lama_hari"],
    "produk": ["produk", "barang", "item", "sku", "layanan"],
    "jenis": ["jenis", "tipe", "type"],
    "tenggat": ["tenggat_jam", "sisa_jam", "batas_jam", "sisa_waktu_jam"],
}

# Kategori penyebab (akar masalah). retur_refund hanya jadi utama bila tidak ada penyebab lain.
KATA = {
    "belum_sampai": ["belum sampai", "belum diterima", "belum datang", "tidak sampai", "gak sampai", "ga sampai", "nggak sampai",
                     "kok lama", "lama banget", "resi tidak", "resi ga", "tidak bergerak", "macet", "stuck", "nyangkut",
                     "kapan sampai", "paket hilang", "barang hilang", "sudah seminggu", "sudah sebulan", "sampai sekarang belum"],
    "rusak_tidak_sesuai": ["rusak", "pecah", "cacat", "sobek", "jahitan lepas", "jahitannya lepas", "bocor", "penyok", "lecet", "bolong", "luntur", "tidak sesuai",
                           "gak sesuai", "ga sesuai", "nggak sesuai", "beda dengan foto", "beda sama foto", "tidak seperti foto",
                           "kualitas jelek", "kualitasnya jelek", "bau", "kotor", "mati total", "tidak menyala", "tidak berfungsi",
                           "ngelupas", "mengelupas", "kusut", "tipis banget", "palsu", "kw", "bukan original", "tidak original"],
    "salah_kirim": ["salah kirim", "bukan pesanan", "bukan yang saya pesan", "beda barang", "salah warna", "salah ukuran",
                    "salah varian", "salah size", "ukurannya salah", "ukuran salah", "warnanya salah", "warna salah", "varian salah", "yang datang berbeda", "kurang item", "kurang satu", "kurang 1", "tidak lengkap",
                    "ga lengkap", "gak lengkap", "kurang pcs", "isi paket kosong", "paket kosong"],
    "cod_gagal": ["cod ditolak", "cod saya ditolak", "ditolak kurir", "kembali ke penjual", "balik ke penjual", "tolak cod", "cod gagal", "gagal kirim", "gagal antar", "tidak ada di rumah", "paket kembali",
                  "dikembalikan ke penjual", "retur ke pengirim", "dikembalikan ke pengirim", "kurir tidak bisa menghubungi",
                  "tidak bisa dihubungi", "penerima menolak", "ditolak penerima", "bayar di tempat", "tidak jadi terima"],
    "komplain_layanan": ["admin lambat", "slow respon", "slow respons", "lambat balas", "tidak dibalas", "ga dibalas", "gak dibalas",
                         "tidak ada respon", "tidak direspon", "dicuekin", "diabaikan", "judes", "tidak ramah", "pelayanan buruk",
                         "pelayanan jelek", "pelayanan lambat", "kemasan jelek", "kemasan asal", "packing jelek", "packing asal",
                         "packing tipis", "packing tidak rapi", "tidak jujur", "bohong"],
    "retur_refund": ["retur", "refund", "pengembalian dana", "kembalikan uang", "uang kembali", "minta ganti", "ganti baru",
                     "tukar", "batalkan pesanan", "cancel", "balikin uang", "mau balikin", "dikembalikan dana"],
}
PERTANYAAN = ["apakah", "apa ", "bisa", "ready", "stok", "ongkir", "berapa", "kapan", "gimana", "bagaimana", "boleh", "?"]
NEGATIF = ["kecewa", "jelek", "buruk", "mengecewakan", "parah", "zonk", "kapok", "menyesal", "tidak puas", "sebel", "kesal", "marah", "payah"]
POSITIF = ["bagus", "puas", "mantap", "recommended", "rekomen", "cepat", "ramah", "terima kasih", "makasih", "sesuai pesanan", "oke banget"]
AMAN = ["alergi", "iritasi", "keracunan", "basi", "kadaluarsa", "kedaluwarsa", "expired", "melepuh", "luka", "berbahaya",
        "sakit perut", "muntah", "tersengat", "korsleting", "kebakar", "terbakar", "gatal", "ruam", "bengkak", "diare"]
ANCAMAN = ["lapor", "laporkan", "bintang 1", "bintang satu", "kasih bintang", "ulasan buruk", "review jelek", "review buruk", "viral",
           "bpsk", "polisi", "pengacara", "somasi", "pengadilan", "media sosial", "boikot", "bad review", "akan saya tulis",
           "saya tulis di", "bongkar", "tuntut", "gugat", "tipu", "ditipu", "menipu", "penipu", "penipuan", "scam"]
ULANG = ["berkali-kali", "berkali kali", "sudah chat", "sudah tanya", "sudah 3 kali", "sudah dua kali", "sudah 2 kali",
         "tidak ada kabar", "ga ada kabar", "gak ada kabar", "dari kemarin", "dari minggu lalu", "ditanya terus"]

URUTAN_SERI = ["belum_sampai", "rusak_tidak_sesuai", "salah_kirim", "cod_gagal", "komplain_layanan", "retur_refund"]
NAMA = {
    "belum_sampai": "belum sampai / kurir",
    "rusak_tidak_sesuai": "barang rusak / tidak sesuai",
    "salah_kirim": "salah kirim / barang kurang",
    "cod_gagal": "COD gagal / ditolak",
    "komplain_layanan": "komplain layanan",
    "retur_refund": "minta retur / refund",
    "pertanyaan": "pertanyaan biasa (bukan keluhan)",
    "kecewa_umum": "kecewa, sebab belum jelas (perlu dibaca)",
    "bukan_keluhan": "bukan keluhan",
}
# Kata singkat harus cocok sebagai kata utuh (mis. "kw", "bau", "cancel")
KATA_UTUH = {"kw", "bau", "cancel", "tukar", "lapor", "tipu", "scam", "luka", "gatal", "ruam", "macet", "stuck", "viral", "bpsk",
             "ready", "stok", "bisa", "apa", "apakah", "polisi", "retur", "refund", "muntah", "diare", "basi", "rusak", "pecah",
             "sobek", "bocor", "bolong", "lecet", "luntur", "kotor", "palsu", "cacat"}


class GalatInput(Exception):
    pass


def _norm(teks):
    return re.sub(r"\s+", " ", (teks or "").lower()).strip()


def _punya(teks, kata):
    if kata in KATA_UTUH:
        return re.search(r"(?<![a-z0-9])" + re.escape(kata) + r"(?![a-z0-9])", teks) is not None
    return kata in teks


def _hitung(teks, daftar):
    return [k for k in daftar if _punya(teks, k)]


def baca_angka(nilai):
    """'Rp129.000', '129rb', '1,5jt', '129000' -> Decimal; None bila bukan angka."""
    t = (nilai or "").strip().lower().replace("rp", "").replace(" ", "")
    if not t:
        return None
    pengali = Decimal(1)
    for akhiran, kali in (("juta", 10**6), ("jt", 10**6), ("ribu", 10**3), ("rb", 10**3), ("k", 10**3)):
        if t.endswith(akhiran):
            pengali, t = Decimal(kali), t[: -len(akhiran)]
            break
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", t):
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", t):
        t = t.replace(",", "")
    else:
        t = t.replace(",", ".")
    try:
        angka = Decimal(t) * pengali
    except InvalidOperation:
        return None
    if angka.is_nan() or angka.is_infinite() or angka < 0 or angka > Decimal("1e12"):
        return None
    return angka


def samarkan(teks):
    t = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email]", teks or "")
    t = re.sub(r"(?<!\d)(\+?62|0)[\d\s\-.]{7,14}\d", "[nomor]", t)
    t = re.sub(r"\d{9,}", "[angka-panjang]", t)
    return t


def _peta_kolom(header):
    kunci = {re.sub(r"[\s\-]+", "_", (h or "").strip().lower().lstrip("﻿")): i for i, h in enumerate(header)}
    peta = {}
    for logis, daftar in ALIAS.items():
        for nama in daftar:
            if nama in kunci:
                peta[logis] = kunci[nama]
                break
    return peta


def baca_csv(teks):
    if not teks.strip():
        raise GalatInput("Berkas kosong.")
    contoh = teks[:4096]
    try:
        pemisah = csv.Sniffer().sniff(contoh, delimiters=",;\t|").delimiter
    except csv.Error:
        pemisah = ","
    baris = list(csv.reader(io.StringIO(teks), delimiter=pemisah))
    baris = [b for b in baris if any((c or "").strip() for c in b)]
    if len(baris) < 2:
        raise GalatInput("Berkas hanya berisi satu baris; butuh judul kolom dan minimal satu keluhan.")
    peta = _peta_kolom(baris[0])
    if "pesan" not in peta:
        raise GalatInput("Kolom isi keluhan tidak ditemukan. Beri judul kolom 'pesan' (atau isi/keluhan/ulasan/komentar/chat).")
    return peta, baris[1:]


def klasifikasi(pesan, bintang=None, nilai=None, menunggu=None, tenggat=None, ulasan_publik=False, nilai_besar=NILAI_BESAR_DEFAULT):
    t = _norm(pesan)
    skor = {k: len(_hitung(t, KATA[k])) for k in KATA}
    akar = {k: v for k, v in skor.items() if v and k != "retur_refund"}
    permintaan_retur = skor["retur_refund"] > 0
    if akar:
        urut = sorted(akar, key=lambda k: (-akar[k], URUTAN_SERI.index(k)))
        utama, sekunder = urut[0], urut[1:]
    elif permintaan_retur:
        utama, sekunder = "retur_refund", []
    else:
        utama, sekunder = None, []
    if utama is None:
        if _hitung(t, NEGATIF) or (bintang is not None and bintang <= 2):
            utama = "kecewa_umum"
        elif _hitung(t, PERTANYAAN) or (bintang is None):
            utama = "pertanyaan"
        else:
            utama = "bukan_keluhan"
    if utama in ("komplain_layanan", "kecewa_umum") and _hitung(t, POSITIF) and not _hitung(t, NEGATIF) \
            and not (bintang is not None and bintang <= 3):
        utama, sekunder = "bukan_keluhan", []
    if utama in ("belum_sampai", "rusak_tidak_sesuai", "salah_kirim", "cod_gagal", "retur_refund"):
        if permintaan_retur and utama != "retur_refund":
            sekunder = sekunder + ["retur_refund"]

    aman = _hitung(t, AMAN)
    ancam = _hitung(t, ANCAMAN)
    ulang = _hitung(t, ULANG)
    alasan, tanda = [], []
    if utama in ("pertanyaan", "bukan_keluhan") and (aman or ancam):
        utama = "kecewa_umum"

    dasar = {"belum_sampai": 2, "rusak_tidak_sesuai": 2, "salah_kirim": 2, "cod_gagal": 2, "retur_refund": 2,
             "komplain_layanan": 3, "kecewa_umum": 3, "pertanyaan": 3, "bukan_keluhan": 3}[utama]
    level = dasar
    if ulasan_publik and bintang is not None and bintang <= 2 and level > 2:
        level = 2
        alasan.append("ulasan publik bintang 1-2 (tampak oleh calon pembeli)")
    if aman and utama not in ("pertanyaan", "bukan_keluhan"):
        level = 1
        alasan.append("menyebut keamanan/kesehatan: " + ", ".join(aman[:3]))
        tanda.append("keamanan")
    if ancam and utama not in ("pertanyaan", "bukan_keluhan"):
        level = 1
        alasan.append("ada ancaman/tuduhan: " + ", ".join(ancam[:3]))
        tanda.append("ancaman_reputasi")
    if tenggat is not None and tenggat <= 24:
        level = 1
        alasan.append(f"tenggat platform tinggal {tenggat:g} jam")
        tanda.append("tenggat_platform")
    naik = 0
    if nilai is not None and nilai >= nilai_besar and utama not in ("pertanyaan", "bukan_keluhan"):
        naik += 1
        alasan.append("nilai pesanan besar")
        tanda.append("nilai_besar")
    if menunggu is not None and menunggu >= 2 and utama not in ("pertanyaan", "bukan_keluhan"):
        naik += 1
        alasan.append(f"sudah menunggu {menunggu:g} hari")
    if ulang and utama not in ("pertanyaan", "bukan_keluhan"):
        naik += 1
        alasan.append("pelanggan mengulang keluhan")
    level = max(1, level - min(naik, 1))
    if not alasan:
        alasan.append("jenis keluhan: " + NAMA[utama])
    if utama in ("pertanyaan", "bukan_keluhan") and not (ancam or aman):
        level = 3
    return {"kategori": utama, "kategori_nama": NAMA[utama], "kategori_lain": sekunder, "prioritas": f"P{level}",
            "alasan": alasan, "tanda": tanda}


def proses(teks_csv, nilai_besar=NILAI_BESAR_DEFAULT):
    peta, baris = baca_csv(teks_csv)
    dipotong = len(baris) > MAKS_BARIS
    baris = baris[:MAKS_BARIS]

    def sel(b, kunci):
        i = peta.get(kunci)
        return b[i].strip() if i is not None and i < len(b) else ""

    hasil, kosong = [], 0
    for n, b in enumerate(baris, start=1):
        pesan = sel(b, "pesan")
        if not pesan:
            kosong += 1
            continue
        try:
            bintang = float(sel(b, "bintang").replace(",", ".")) if sel(b, "bintang") else None
            if bintang is not None and not (0 <= bintang <= 5):
                bintang = None
        except ValueError:
            bintang = None
        nilai = baca_angka(sel(b, "nilai"))
        try:
            menunggu = float(sel(b, "menunggu").replace(",", ".")) if sel(b, "menunggu") else None
        except ValueError:
            menunggu = None
        try:
            tenggat = float(sel(b, "tenggat").replace(",", ".")) if sel(b, "tenggat") else None
        except ValueError:
            tenggat = None
        jenis = _norm(sel(b, "jenis"))
        publik = ("ulasan" in jenis or "review" in jenis) if jenis else bintang is not None
        r = klasifikasi(pesan, bintang, nilai, menunggu, tenggat, publik, nilai_besar)
        r.update({"kode": f"K{len(hasil) + 1}", "baris": n + 1, "id_sumber": samarkan(sel(b, "id")) or None,
                  "platform": sel(b, "platform") or None, "produk": sel(b, "produk") or None,
                  "nilai": int(nilai) if nilai is not None else None, "bintang": bintang,
                  "cuplikan": samarkan(pesan)[:90]})
        hasil.append(r)

    # keluhan ganda dari satu pesanan (id sama) digabung ke penanda
    hitung_id = Counter(r["id_sumber"] for r in hasil if r["id_sumber"])
    for r in hasil:
        if r["id_sumber"] and hitung_id[r["id_sumber"]] > 1:
            r["tanda"].append("pesanan_ganda")
            r["alasan"].append("pesanan yang sama muncul lebih dari sekali")
    # pola: >= 3 keluhan dengan penyebab (dan produk bila ada) sama
    kunci_pola = Counter((r["kategori"], r["produk"]) for r in hasil if r["kategori"] not in ("pertanyaan", "bukan_keluhan", "kecewa_umum"))
    pola = [{"kategori": NAMA[k], "produk": p, "jumlah": j} for (k, p), j in kunci_pola.items() if j >= 3]
    for r in hasil:
        if any(p["kategori"] == NAMA[r["kategori"]] and p["produk"] == r["produk"] for p in pola):
            r["tanda"].append("pola")

    urut = sorted(hasil, key=lambda r: (int(r["prioritas"][1]), -(r["nilai"] or 0), r["bintang"] if r["bintang"] is not None else 9))
    for r in hasil:
        r["eskalasi_pemilik"] = bool({"keamanan", "ancaman_reputasi", "nilai_besar", "tenggat_platform"} & set(r["tanda"]))
    per_kat = Counter(r["kategori_nama"] for r in hasil)
    per_pri = Counter(r["prioritas"] for r in hasil)
    return {
        "jumlah_keluhan": len(hasil),
        "baris_kosong_dilewati": kosong,
        "dipotong_maks_baris": dipotong,
        "per_prioritas": {k: per_pri.get(k, 0) for k in ("P1", "P2", "P3")},
        "per_kategori": dict(per_kat.most_common()),
        "pola": pola,
        "perlu_pemilik": [r["kode"] for r in urut if r["eskalasi_pemilik"]],
        "urutan_kerja": [r["kode"] for r in urut],
        "keluhan": hasil,
        "ringkasan_untuk_agent": "UNTUK AGENT SAJA, jangan tampilkan ke pengguna. Hasil ini dugaan kata kunci; baca ulang pesan asli "
                                 "sebelum memutuskan. Jangan salin nomor/nama pelanggan ke rekap grup.",
    }


def _baca_berkas(path):
    try:
        mentah = open(path, "rb").read()
    except FileNotFoundError:
        raise GalatInput(f"Berkas tidak ditemukan: {path}")
    except (IsADirectoryError, PermissionError) as e:
        raise GalatInput(f"Berkas tidak bisa dibuka: {e.__class__.__name__}")
    if b"\x00" in mentah[:4096]:
        raise GalatInput("Berkas bukan teks CSV (tampaknya Excel/biner). Simpan ulang sebagai CSV UTF-8.")
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return mentah.decode(enc)
        except UnicodeDecodeError:
            continue
    raise GalatInput("Encoding berkas tidak dikenali.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Pra-pilah keluhan pelanggan dari CSV.")
    p.add_argument("berkas")
    p.add_argument("--nilai-besar", default="500000", help="batas nilai pesanan 'besar' (rupiah), default 500000")
    p.add_argument("--format", choices=["json", "ringkas"], default="json")
    a = p.parse_args(argv)
    batas = baca_angka(a.nilai_besar)
    if batas is None or batas <= 0:
        print("Galat: --nilai-besar harus angka rupiah positif.", file=sys.stderr)
        return 2
    try:
        hasil = proses(_baca_berkas(a.berkas), batas)
    except GalatInput as e:
        print(f"Galat: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(hasil["ringkasan_untuk_agent"])
        print(f"Jumlah keluhan: {hasil['jumlah_keluhan']} | {hasil['per_prioritas']}")
        for k, v in hasil["per_kategori"].items():
            print(f"  {k}: {v}")
        print("Perlu pemilik:", ", ".join(hasil["perlu_pemilik"]) or "-")
        for pl in hasil["pola"]:
            print(f"Pola: {pl['jumlah']}x {pl['kategori']}" + (f" ({pl['produk']})" if pl["produk"] else ""))
        for kode in hasil["urutan_kerja"]:
            r = next(x for x in hasil["keluhan"] if x["kode"] == kode)
            print(f"{kode} {r['prioritas']} {r['kategori_nama']} - " + "; ".join(r["alasan"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
