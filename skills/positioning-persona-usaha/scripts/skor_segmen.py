#!/usr/bin/env python3
"""Skor & urutkan segmen pelanggan dengan matriks berbobot (Python standar saja).

Pakai:
  python3 scripts/skor_segmen.py segmen.csv
  python3 scripts/skor_segmen.py segmen.csv --bobot "daya_beli=30,persaingan=5"
  python3 scripts/skor_segmen.py segmen.csv --format json
(Windows: ganti python3 dengan python atau py.)

CSV: kolom `segmen` + kolom kriteria, nilai 1-5 (5 = paling menguntungkan bagi usaha).
Kriteria baku dan bobot awal (jumlah 100):
  ukuran 15, daya_beli 20, kebutuhan 20, jangkauan_kanal 15, kecocokan_produk 15, persaingan 10, kemampuan_layani 5
Catatan arah: persaingan 5 = sedikit pesaing / mudah menonjol; jangkauan_kanal 5 = mudah dijangkau.
Skor = jumlah(bobot x nilai) / jumlah(bobot) x 20  -> skala 0-100.
Keluar kode 0 bila sukses, 2 bila input salah (pesan jelas di stderr).
"""
import argparse
import csv
import json
import sys

KRITERIA = ["ukuran", "daya_beli", "kebutuhan", "jangkauan_kanal", "kecocokan_produk",
            "persaingan", "kemampuan_layani"]
BOBOT_AWAL = {"ukuran": 15, "daya_beli": 20, "kebutuhan": 20, "jangkauan_kanal": 15,
              "kecocokan_produk": 15, "persaingan": 10, "kemampuan_layani": 5}


class InputSalah(Exception):
    pass


def baca_bobot(teks):
    bobot = dict(BOBOT_AWAL)
    if not teks:
        return bobot
    for bagian in teks.split(","):
        if not bagian.strip():
            continue
        if "=" not in bagian:
            raise InputSalah(f"Bobot '{bagian}' salah format; pakai nama=angka, mis. daya_beli=30")
        k, v = (x.strip() for x in bagian.split("=", 1))
        if k not in KRITERIA:
            raise InputSalah(f"Kriteria '{k}' tidak dikenal. Pilihan: {', '.join(KRITERIA)}")
        try:
            angka = float(v.replace(",", "."))
        except ValueError:
            raise InputSalah(f"Bobot '{k}' bukan angka: '{v}'")
        if angka < 0:
            raise InputSalah(f"Bobot '{k}' tidak boleh negatif")
        bobot[k] = angka
    if sum(bobot.values()) <= 0:
        raise InputSalah("Jumlah bobot harus lebih dari 0")
    return bobot


def baca_csv(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            teks = f.read()
    except FileNotFoundError:
        raise InputSalah(f"File tidak ditemukan: {path}")
    except UnicodeDecodeError:
        raise InputSalah("File harus berkode UTF-8 (simpan ulang sebagai CSV UTF-8)")
    if not teks.strip():
        raise InputSalah("File kosong")
    pemisah = ";" if teks.splitlines()[0].count(";") > teks.splitlines()[0].count(",") else ","
    baca = csv.DictReader(teks.splitlines(), delimiter=pemisah)
    kolom = [(c or "").strip().lower() for c in (baca.fieldnames or [])]
    if "segmen" not in kolom:
        raise InputSalah("Kolom 'segmen' tidak ada di baris judul")
    hilang = [k for k in KRITERIA if k not in kolom]
    if hilang:
        raise InputSalah("Kolom kriteria kurang: " + ", ".join(hilang))
    baris = []
    for no, r in enumerate(baca, start=2):
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        if not any(r.values()):
            continue
        baris.append((no, r))
    if not baris:
        raise InputSalah("Tidak ada baris segmen")
    return baris


def hitung(baris, bobot):
    total_bobot = sum(bobot.values())
    hasil, dilihat = [], set()
    for no, r in baris:
        nama = r["segmen"]
        if not nama:
            raise InputSalah(f"Baris {no}: nama segmen kosong")
        if nama.lower() in dilihat:
            raise InputSalah(f"Baris {no}: nama segmen '{nama}' ganda")
        dilihat.add(nama.lower())
        nilai = {}
        for k in KRITERIA:
            mentah = r[k].replace(",", ".")
            try:
                n = float(mentah)
            except ValueError:
                raise InputSalah(f"Baris {no} ({nama}): '{k}' harus angka 1-5, ditemukan '{r[k]}'")
            if not 1 <= n <= 5:
                raise InputSalah(f"Baris {no} ({nama}): '{k}' harus 1-5, ditemukan {r[k]}")
            nilai[k] = n
        skor = sum(bobot[k] * nilai[k] for k in KRITERIA) / total_bobot * 20
        hasil.append({"segmen": nama, "skor": round(skor + 1e-9, 1), "nilai": nilai})
    hasil.sort(key=lambda h: (-h["skor"], -h["nilai"]["daya_beli"], h["segmen"].lower()))
    for i, h in enumerate(hasil, start=1):
        h["peringkat"] = i
        if h["skor"] >= 75:
            h["saran"] = "Utama (layani duluan)"
        elif h["skor"] >= 60:
            h["saran"] = "Kandidat (uji kecil dulu)"
        else:
            h["saran"] = "Tunda"
        lemah = [k for k in KRITERIA if h["nilai"][k] <= 2]
        h["titik_lemah"] = lemah
    return hasil


def main(argv=None):
    ap = argparse.ArgumentParser(description="Skor segmen pelanggan berbobot")
    ap.add_argument("csv")
    ap.add_argument("--bobot", default="", help='ubah bobot, mis. "daya_beli=30,persaingan=5"')
    ap.add_argument("--format", choices=["tabel", "json"], default="tabel")
    a = ap.parse_args(argv)
    try:
        bobot = baca_bobot(a.bobot)
        hasil = hitung(baca_csv(a.csv), bobot)
    except InputSalah as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps({"bobot": bobot, "hasil": hasil}, ensure_ascii=False, indent=2))
        return 0
    print("Bobot: " + ", ".join(f"{k} {bobot[k]:g}" for k in KRITERIA))
    print(f"{'#':<3}{'Segmen':<34}{'Skor':>6}  Saran")
    for h in hasil:
        lemah = f"  [lemah: {', '.join(h['titik_lemah'])}]" if h["titik_lemah"] else ""
        print(f"{h['peringkat']:<3}{h['segmen'][:33]:<34}{h['skor']:>6.1f}  {h['saran']}{lemah}")
    print("Skor 0-100 dari penilaian 1-5 (penilaian = perkiraan, bukan data pasar). Pilih 1 segmen utama, maks. 2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
