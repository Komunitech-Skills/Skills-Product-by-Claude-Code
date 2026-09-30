#!/usr/bin/env python3
"""Skor & urutkan calon nama usaha/produk dengan matriks berbobot (Python standar saja).

Pakai:
  python3 scripts/skor_nama.py nama.csv --merek "Indomie, Kopi Kenangan"
  python3 scripts/skor_nama.py nama.csv --merek-file merek.txt --bobot "kemiripan=30,khas=10"
  python3 scripts/skor_nama.py nama.csv --format json
  python3 scripts/skor_nama.py --hitung "Sambal Nusa"      # panjang & suku kata satu nama
(Windows: ganti python3 dengan python atau py.)

CSV: kolom `nama` (wajib) + kolom penilaian manual 1-5 (kosong = 3, ditandai "belum dinilai"):
  aman_makna  5 = tidak ada arti negatif/lucu di bahasa Indonesia, daerah, atau slang
  khas        5 = jelas beda dari pesaing yang dikenal
  relevan     5 = langsung mengingatkan pada produk/manfaat
Otomatis dihitung script: panjang, suku_kata, ejaan, kemiripan (terhadap daftar merek yang DIBERIKAN pengguna).
Bobot awal (jumlah 100): panjang 10, suku_kata 10, ejaan 10, kemiripan 20, aman_makna 20, khas 15, relevan 15.
Skor = jumlah(bobot x nilai) / jumlah(bobot) x 20 -> skala 0-100. Bobot memakai TITIK untuk desimal.
Nama dengan koma wajib diberi tanda kutip di CSV.
Tanda TANDAI (nama tidak boleh dipilih sebelum diperiksa): kemiripan terlalu tinggi dengan merek yang diberikan,
atau aman_makna = 1. Script TIDAK memeriksa ketersediaan domain/handle/merek terdaftar dan tidak mendengar bunyi
(kemiripan = kemiripan ejaan saja). Dua nama teratas selisih <= 5 poin = SETARA.
Keluar kode 0 bila sukses, 2 bila input salah (pesan jelas di stderr).
"""
import argparse
import csv
import difflib
import json
import re
import sys

KRITERIA = ["panjang", "suku_kata", "ejaan", "kemiripan", "aman_makna", "khas", "relevan"]
MANUAL = ["aman_makna", "khas", "relevan"]
BOBOT_AWAL = {"panjang": 10, "suku_kata": 10, "ejaan": 10, "kemiripan": 20,
              "aman_makna": 20, "khas": 15, "relevan": 15}
BATAS_SERI = 5.0
MAKS_NAMA = 100
VOKAL = set("aiueo")
DIFTONG = ("ai", "au", "oi")


class InputSalah(Exception):
    pass


def huruf(teks):
    return re.sub(r"[^a-z]", "", teks.lower())


def suku_kata_kata(kata):
    """Hitung suku kata satu kata. Tiap huruf vokal = 1 suku kata, kecuali diftong ai/au/oi
    (dihitung 1). Kata tanpa vokal (singkatan mis. BCA) dibaca per huruf."""
    k = re.sub(r"[^a-z]", "", kata.lower())
    if not k:
        return 0
    if not any(c in VOKAL for c in k):
        return len(k)
    n, i = 0, 0
    while i < len(k):
        if k[i] in VOKAL:
            n += 1
            if k[i:i + 2] in DIFTONG:
                i += 1
        i += 1
    return n


def suku_kata(nama):
    return sum(suku_kata_kata(k) for k in re.split(r"\s+", nama.strip()) if k)


def skor_panjang(n):
    if n < 3:
        return 2
    if n <= 8:
        return 5
    if n <= 10:
        return 4
    if n <= 12:
        return 3
    if n <= 15:
        return 2
    return 1


def skor_suku(n):
    if n in (2, 3):
        return 5
    if n == 4:
        return 4
    if n == 1:
        return 3
    if n == 5:
        return 2
    return 1


def skor_ejaan(nama):
    """5 = mudah dieja. Kurangi: angka/simbol (-2), huruf sama 3x berturut (-1),
    3 konsonan berturut di luar ng/ny/sy/kh (-1), huruf q/x (-1). Minimum 1."""
    s, alasan = 5, []
    if re.search(r"[^A-Za-z\s]", nama):
        s -= 2
        alasan.append("ada angka/simbol")
    low = nama.lower()
    if re.search(r"([a-z])\1\1", low):
        s -= 1
        alasan.append("huruf sama 3x")
    bersih = re.sub(r"ng|ny|sy|kh|gh", "a", low)
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{3}", re.sub(r"[^a-z]", " ", bersih)):
        s -= 1
        alasan.append("3 konsonan berturut")
    if re.search(r"[qx]", low):
        s -= 1
        alasan.append("huruf q/x")
    return max(s, 1), alasan


def kemiripan(nama, merek):
    """Kembalikan (skor 1-5, merek paling mirip, rasio). Rasio = difflib pada huruf saja."""
    a = huruf(nama)
    terbaik, rasio_max = "", 0.0
    for m in merek:
        b = huruf(m)
        if not a or not b:
            continue
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if min(len(a), len(b)) >= 4 and (a in b or b in a):
            r = max(r, 0.9)
        if r > rasio_max:
            rasio_max, terbaik = r, m
    if rasio_max >= 0.85:
        s = 1
    elif rasio_max >= 0.75:
        s = 2
    elif rasio_max >= 0.65:
        s = 3
    elif rasio_max >= 0.5:
        s = 4
    else:
        s = 5
    return s, terbaik, rasio_max


def baca_bobot(teks):
    bobot = dict(BOBOT_AWAL)
    if not teks:
        return bobot
    for bagian in teks.split(","):
        if not bagian.strip():
            continue
        if "=" not in bagian:
            raise InputSalah(f"bobot '{bagian.strip()}' harus berbentuk kriteria=angka")
        k, v = (x.strip() for x in bagian.split("=", 1))
        if k not in KRITERIA:
            raise InputSalah(f"kriteria bobot '{k}' tidak dikenal. Pilihan: {', '.join(KRITERIA)}")
        try:
            angka = float(v)
        except ValueError:
            raise InputSalah(f"bobot '{k}' bukan angka: '{v}' (desimal pakai titik)")
        if angka != angka or angka in (float("inf"), float("-inf")) or angka < 0:
            raise InputSalah(f"bobot '{k}' harus angka 0 atau lebih")
        bobot[k] = angka
    if sum(bobot.values()) <= 0:
        raise InputSalah("jumlah bobot harus lebih dari 0")
    return bobot


def daftar_merek(teks, path):
    hasil = []
    if teks:
        hasil += [x.strip() for x in re.split(r"[,;\n]", teks) if x.strip()]
    if path:
        try:
            with open(path, encoding="utf-8-sig") as f:
                hasil += [x.strip() for x in f.read().splitlines() if x.strip()]
        except (OSError, UnicodeDecodeError) as e:
            raise InputSalah(f"tidak bisa membaca file merek '{path}': {e}")
    return hasil


def baca_csv(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            baris = list(csv.reader(f))
    except (OSError, UnicodeDecodeError) as e:
        raise InputSalah(f"tidak bisa membaca '{path}': {e} (simpan CSV sebagai UTF-8)")
    baris = [b for b in baris if any(c.strip() for c in b)]
    if not baris:
        raise InputSalah("file CSV kosong")
    kepala = [h.strip().lower() for h in baris[0]]
    if "nama" not in kepala:
        raise InputSalah("kolom 'nama' tidak ada di baris pertama CSV")
    for h in kepala:
        if h != "nama" and h not in MANUAL:
            raise InputSalah(f"kolom '{h}' tidak dikenal. Kolom boleh: nama, {', '.join(MANUAL)}")
    if len(set(kepala)) != len(kepala):
        raise InputSalah("ada kolom ganda di baris pertama CSV")
    data = []
    for no, b in enumerate(baris[1:], start=2):
        if len(b) > len(kepala):
            raise InputSalah(f"baris {no}: kolom lebih banyak dari judul (nama berkoma harus diberi tanda kutip)")
        b = b + [""] * (len(kepala) - len(b))
        r = dict(zip(kepala, (c.strip() for c in b)))
        if not r["nama"]:
            raise InputSalah(f"baris {no}: nama kosong")
        for k in MANUAL:
            v = r.get(k, "")
            if v == "":
                r[k] = None
                continue
            try:
                x = float(v)
            except ValueError:
                raise InputSalah(f"baris {no}: '{k}' bukan angka: '{v}'")
            if x != int(x) or not 1 <= x <= 5:
                raise InputSalah(f"baris {no}: '{k}' harus bilangan bulat 1-5, bukan '{v}'")
            r[k] = int(x)
        data.append(r)
    if not data:
        raise InputSalah("CSV tidak berisi nama (hanya judul kolom)")
    if len(data) > MAKS_NAMA:
        raise InputSalah(f"terlalu banyak nama ({len(data)}); maksimal {MAKS_NAMA}")
    lihat = {}
    for r in data:
        kunci = huruf(r["nama"]) or r["nama"].lower()
        if kunci in lihat:
            raise InputSalah(f"nama ganda: '{lihat[kunci]}' dan '{r['nama']}'")
        lihat[kunci] = r["nama"]
    return data


def nilai(data, merek, bobot):
    hasil = []
    total_bobot = sum(bobot.values())
    for r in data:
        nama = r["nama"]
        nilai_k, catatan, tandai = {}, [], []
        nilai_k["panjang"] = skor_panjang(len(huruf(nama)))
        sk = suku_kata(nama)
        nilai_k["suku_kata"] = skor_suku(sk)
        e, alasan = skor_ejaan(nama)
        nilai_k["ejaan"] = e
        if alasan:
            catatan.append("ejaan: " + ", ".join(alasan))
        if merek:
            m, terdekat, rasio = kemiripan(nama, merek)
            nilai_k["kemiripan"] = m
            if m <= 2:
                catatan.append(f"mirip '{terdekat}' ({rasio:.0%} ejaan)")
            if m == 1:
                tandai.append(f"terlalu mirip '{terdekat}'")
        else:
            nilai_k["kemiripan"] = 3
            catatan.append("kemiripan belum diperiksa (tidak ada daftar merek)")
        for k in MANUAL:
            if r[k] is None:
                nilai_k[k] = 3
                catatan.append(f"{k} belum dinilai (dianggap 3)")
            else:
                nilai_k[k] = r[k]
        if nilai_k["aman_makna"] == 1:
            tandai.append("arti/konotasi negatif")
        skor = sum(bobot[k] * nilai_k[k] for k in KRITERIA) / total_bobot * 20
        hasil.append({"nama": nama, "huruf": len(huruf(nama)), "suku_kata": sk, "nilai": nilai_k,
                      "skor": round(skor, 1), "tandai": tandai, "catatan": catatan})
    hasil.sort(key=lambda x: (-x["skor"], x["nama"].lower()))
    layak = [x for x in hasil if not x["tandai"]]
    seri = len(layak) >= 2 and (layak[0]["skor"] - layak[1]["skor"]) <= BATAS_SERI
    return hasil, seri


def cetak_teks(hasil, seri, bobot, merek):
    print(f"Bobot: " + ", ".join(f"{k}={bobot[k]:g}" for k in KRITERIA))
    print(f"Merek pembanding: {', '.join(merek) if merek else '(tidak ada)'}")
    print()
    print(f"{'#':>2}  {'Nama':<24}{'Skor':>6}  {'Huruf':>5} {'Suku':>4}  Status / catatan")
    for i, x in enumerate(hasil, 1):
        st = "TANDAI: " + "; ".join(x["tandai"]) if x["tandai"] else "layak dicek"
        cat = ("; " + "; ".join(x["catatan"])) if x["catatan"] else ""
        print(f"{i:>2}  {x['nama'][:23]:<24}{x['skor']:>6.1f}  {x['huruf']:>5} {x['suku_kata']:>4}  {st}{cat}")
    layak = [x for x in hasil if not x["tandai"]]
    print()
    if not layak:
        print("Semua nama ditandai. Buat opsi baru.")
    elif seri:
        print(f"SETARA: '{layak[0]['nama']}' dan '{layak[1]['nama']}' selisih <= {BATAS_SERI:g} poin. "
              "Pilih lewat uji ucap ke 5 orang dan cek ketersediaan.")
    else:
        print(f"Teratas yang layak dicek: '{layak[0]['nama']}' ({layak[0]['skor']:.1f}/100).")
    print("Ingat: skor ini bukan bukti nama tersedia. Cek domain, handle, dan merek (PDKI) sendiri.")


def hitung_satu(nama):
    e, alasan = skor_ejaan(nama)
    print(f"Nama: {nama}")
    print(f"Huruf (tanpa spasi/simbol): {len(huruf(nama))}; suku kata: {suku_kata(nama)}")
    print(f"Skor panjang {skor_panjang(len(huruf(nama)))}, suku kata {skor_suku(suku_kata(nama))}, "
          f"ejaan {e}" + (f" ({', '.join(alasan)})" if alasan else ""))


def main(argv=None):
    p = argparse.ArgumentParser(description="Skor calon nama usaha/produk", allow_abbrev=False)
    p.add_argument("csv", nargs="?", help="file CSV calon nama")
    p.add_argument("--merek", default="", help="merek yang ingin dibandingkan, dipisah koma")
    p.add_argument("--merek-file", default="", help="file teks berisi satu merek per baris")
    p.add_argument("--bobot", default="", help='mis. "kemiripan=30,khas=10"')
    p.add_argument("--format", choices=["teks", "json", "csv"], default="teks")
    p.add_argument("--hitung", default="", help="hitung panjang & suku kata satu nama")
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        if a.hitung:
            hitung_satu(a.hitung)
            return 0
        if not a.csv:
            raise InputSalah('sebutkan file CSV calon nama, atau pakai --hitung "nama"')
        bobot = baca_bobot(a.bobot)
        merek = daftar_merek(a.merek, a.merek_file)
        hasil, seri = nilai(baca_csv(a.csv), merek, bobot)
    except InputSalah as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps({"bobot": bobot, "merek": merek, "seri": seri, "hasil": hasil},
                         ensure_ascii=False, indent=2))
    elif a.format == "csv":
        w = csv.writer(sys.stdout, lineterminator="\n")
        w.writerow(["peringkat", "nama", "skor"] + KRITERIA + ["status"])
        for i, x in enumerate(hasil, 1):
            w.writerow([i, x["nama"], x["skor"]] + [x["nilai"][k] for k in KRITERIA]
                       + ["TANDAI: " + "; ".join(x["tandai"]) if x["tandai"] else "layak dicek"])
    else:
        cetak_teks(hasil, seri, bobot, merek)
    return 0


if __name__ == "__main__":
    sys.exit(main())
