#!/usr/bin/env python3
"""Skor kualifikasi calon pelanggan (prospek) dari file CSV.

Hanya memakai library standar Python (3.8+). Tidak ada koneksi internet,
tidak membaca file lain selain file CSV yang diberikan lewat argumen.

Kolom yang dibaca dari CSV (nama kolom disesuaikan lewat argumen, semua
nilai berupa angka 0-5 kecuali disebutkan lain):
  --kolom-nama         nama perusahaan/calon pelanggan (wajib, untuk label)
  --kolom-cocok-icp    seberapa cocok profil ideal (0-5)
  --kolom-kebutuhan    seberapa jelas kebutuhannya (0-5)
  --kolom-kemampuan-bayar  perkiraan kemampuan bayar/budget (0-5)
  --kolom-akses-pic    seberapa mudah akses ke pengambil keputusan (0-5)

Bobot default (bisa diubah lewat --bobot cocok_icp,kebutuhan,bayar,akses):
  cocok_icp=0.3, kebutuhan=0.3, bayar=0.2, akses=0.2

Skor akhir 0-100. Kategori: Panas (>=75), Hangat (50-74), Dingin (<50).
"""
import argparse
import csv
import json
import sys

KOLOM_SKOR = ["cocok_icp", "kebutuhan", "bayar", "akses"]
BOBOT_DEFAULT = {"cocok_icp": 0.3, "kebutuhan": 0.3, "bayar": 0.2, "akses": 0.2}


def keluar_error(data):
    print(json.dumps(data, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


def parse_angka_0_5(teks, label, baris_ke):
    teks = (teks or "").strip()
    if not teks:
        return None
    try:
        nilai = float(teks.replace(",", "."))
    except ValueError:
        return None
    if not (0 <= nilai <= 5):
        return None
    return nilai


def baca_csv(path):
    mentah = open(path, "rb").read()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    import io
    try:
        dialek = csv.Sniffer().sniff(teks[:4096], delimiters=",;\t|")
    except csv.Error:
        dialek = csv.excel
    return list(csv.DictReader(io.StringIO(teks), dialect=dialek)), enc


def main():
    p = argparse.ArgumentParser(description="Skor kualifikasi prospek dari CSV")
    p.add_argument("file")
    p.add_argument("--kolom-nama", required=True)
    p.add_argument("--kolom-cocok-icp", required=True)
    p.add_argument("--kolom-kebutuhan", required=True)
    p.add_argument("--kolom-kemampuan-bayar", required=True)
    p.add_argument("--kolom-akses-pic", required=True)
    p.add_argument("--bobot", default="0.3,0.3,0.2,0.2",
                    help="4 angka dipisah koma untuk cocok_icp,kebutuhan,bayar,akses (total idealnya 1.0)")
    a = p.parse_args()

    try:
        bobot_list = [float(x) for x in a.bobot.split(",")]
        if len(bobot_list) != 4:
            raise ValueError
    except ValueError:
        keluar_error({"error": "--bobot harus 4 angka dipisah koma, mis. 0.3,0.3,0.2,0.2"})
    bobot = dict(zip(KOLOM_SKOR, bobot_list))
    total_bobot = sum(bobot.values())
    if abs(total_bobot - 1.0) > 0.01:
        keluar_error({"error": f"Total bobot harus 1.0 (sekarang {total_bobot}). Perbaiki --bobot."})

    try:
        baris, encoding = baca_csv(a.file)
    except OSError as e:
        keluar_error({"error": f"Gagal membaca file: {e}"})

    if not baris:
        keluar_error({"error": "File kosong atau hanya berisi judul kolom"})

    kolom = list(baris[0].keys())
    peta = {
        "cocok_icp": a.kolom_cocok_icp,
        "kebutuhan": a.kolom_kebutuhan,
        "bayar": a.kolom_kemampuan_bayar,
        "akses": a.kolom_akses_pic,
    }
    wajib = [a.kolom_nama] + list(peta.values())
    hilang = [k for k in wajib if k not in kolom]
    if hilang:
        keluar_error({"error": "Kolom tidak ditemukan", "hilang": hilang, "kolom_tersedia": kolom})

    hasil_baris = []
    dilewati = 0
    for i, r in enumerate(baris, start=2):  # baris 1 = header
        nama = (r.get(a.kolom_nama) or "").strip()
        if not nama:
            dilewati += 1
            continue
        nilai = {}
        tidak_valid = False
        for kunci, kolom_nama in peta.items():
            v = parse_angka_0_5(r.get(kolom_nama), kolom_nama, i)
            if v is None:
                tidak_valid = True
                break
            nilai[kunci] = v
        if tidak_valid:
            dilewati += 1
            continue
        skor = sum(nilai[k] * (bobot[k] / 5.0) for k in KOLOM_SKOR) * 100
        skor = round(skor, 1)
        if skor >= 75:
            kategori = "Panas"
        elif skor >= 50:
            kategori = "Hangat"
        else:
            kategori = "Dingin"
        hasil_baris.append({
            "nama": nama,
            "skor": skor,
            "kategori": kategori,
            "rincian": nilai,
        })

    if not hasil_baris:
        keluar_error({"error": "Tidak ada baris valid untuk dihitung", "baris_dilewati": dilewati})

    hasil_baris.sort(key=lambda x: x["skor"], reverse=True)

    hasil = {
        "jumlah_prospek_dihitung": len(hasil_baris),
        "baris_dilewati": dilewati,
        "bobot_dipakai": bobot,
        "ringkasan_kategori": {
            "Panas": sum(1 for x in hasil_baris if x["kategori"] == "Panas"),
            "Hangat": sum(1 for x in hasil_baris if x["kategori"] == "Hangat"),
            "Dingin": sum(1 for x in hasil_baris if x["kategori"] == "Dingin"),
        },
        "prospek": hasil_baris,
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
