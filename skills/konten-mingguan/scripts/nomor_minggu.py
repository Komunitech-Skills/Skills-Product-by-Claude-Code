#!/usr/bin/env python3
"""Hitung kerangka satu minggu (Senin-Minggu) untuk paket konten mingguan: nomor minggu ISO,
tanggal tiap hari, dan penanda momen lokal (gajian, tanggal kembar, hari besar/nasional bertanggal
tetap) supaya AI agent tidak menghitung/mengarang tanggal sendiri.

Momen yang tanggalnya berubah tiap tahun (Ramadan, Lebaran, Imlek, Idul Adha, cuti bersama, libur
sekolah) TIDAK ditebak dan TIDAK ada flag khusus untuk itu di script ini -- agent yang menanyakan ke
pengguna, atau menandai sendiri di teks hasil sebagai "(perkiraan -- cek SKB 3 Menteri/kalender resmi
tahun berjalan)" bila disebutkan tanpa kepastian (lihat SKILL.md).

Hanya library standar Python 3.8+. Lintas OS (Windows: jalankan dengan `python` atau `py`).

Contoh:
  python3 nomor_minggu.py                              # minggu depan (Senin berikutnya) dari hari ini
  python3 nomor_minggu.py --mulai 2026-09-28            # minggu yang dimulai tanggal itu (harus Senin)
  python3 nomor_minggu.py --hari-ini 2026-09-24 --format text
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta

# Windows: pastikan teks Indonesia tercetak tanpa error encoding
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

# (bulan, tanggal): (nama, tipe). tipe: tema | peringatan. Hanya hari besar bertanggal TETAP
# (sama setiap tahun). Referensi umum; skill tetap wajib mengecek kalender resmi tahun berjalan.
MOMEN_TETAP = {
    (1, 1): ("Tahun Baru", "tema"),
    (2, 14): ("Hari Valentine", "tema"),
    (3, 8): ("Hari Perempuan Internasional", "tema"),
    (4, 21): ("Hari Kartini", "tema"),
    (5, 1): ("Hari Buruh", "tema"),
    (5, 2): ("Hari Pendidikan Nasional", "tema"),
    (6, 1): ("Hari Lahir Pancasila", "tema"),
    (7, 23): ("Hari Anak Nasional", "tema"),
    (8, 17): ("HUT Kemerdekaan RI", "tema"),
    (9, 4): ("Hari Pelanggan Nasional", "tema"),
    (9, 30): ("Peringatan G30S", "peringatan"),
    (10, 1): ("Hari Kesaktian Pancasila", "peringatan"),
    (10, 2): ("Hari Batik Nasional", "tema"),
    (10, 22): ("Hari Santri", "tema"),
    (10, 28): ("Hari Sumpah Pemuda", "tema"),
    (11, 10): ("Hari Pahlawan", "peringatan"),
    (11, 25): ("Hari Guru Nasional", "tema"),
    (12, 22): ("Hari Ibu", "tema"),
    (12, 25): ("Hari Natal", "tema"),
    (12, 31): ("Malam Tahun Baru", "tema"),
}


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def parse_tanggal(teks, nama="Tanggal"):
    t = teks.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    galat("{} '{}' tidak dikenali. Pakai format YYYY-MM-DD, mis. 2026-10-05.".format(nama, teks))


def fmt_tgl(d):
    return "{:02d} {} {}".format(d.day, BULAN[d.month], d.year)


def senin_berikutnya(hari_ini):
    """Senin minggu DEPAN dihitung dari hari_ini (bukan minggu berjalan)."""
    sisa = 7 - hari_ini.weekday()  # Senin=0 ... Minggu=6
    return hari_ini + timedelta(days=sisa)


def momen_hari(d, tanggal_gajian):
    daftar = []
    if (d.month, d.day) in MOMEN_TETAP:
        nama, tipe = MOMEN_TETAP[(d.month, d.day)]
        daftar.append({"nama": nama, "tipe": tipe})
    if d.day == d.month and 1 <= d.month <= 12:
        label = "Harbolnas 12.12" if d.month == 12 else "Tanggal kembar {0}.{0}".format(d.month)
        daftar.append({"nama": label, "tipe": "promo"})
    if d.day in tanggal_gajian:
        daftar.append({"nama": "Hari gajian (tgl {})".format(d.day), "tipe": "promo"})
    elif d.day >= 25:
        daftar.append({"nama": "Tanggal tua (mendekati gajian)", "tipe": "info"})
    return daftar


def bangun_minggu(senin, tanggal_gajian):
    hari_list = []
    for i in range(7):
        d = senin + timedelta(days=i)
        hari_list.append({
            "tanggal": d.isoformat(),
            "tanggal_tampil": fmt_tgl(d),
            "hari": HARI[i],
            "momen": momen_hari(d, tanggal_gajian),
        })
    tahun_iso, minggu_iso, _ = senin.isocalendar()
    return {
        "label_minggu": "{}-W{:02d}".format(tahun_iso, minggu_iso),
        "minggu_iso": minggu_iso,
        "tahun_iso": tahun_iso,
        "senin": senin.isoformat(),
        "minggu_terakhir": (senin + timedelta(days=6)).isoformat(),
        "hari": hari_list,
    }


def cetak_text(data):
    print("Minggu {} ({} s.d. {})".format(
        data["label_minggu"], fmt_tgl(datetime.strptime(data["senin"], "%Y-%m-%d").date()),
        fmt_tgl(datetime.strptime(data["minggu_terakhir"], "%Y-%m-%d").date())))
    for h in data["hari"]:
        momen = "; ".join(m["nama"] for m in h["momen"]) or "-"
        print("- {} {} ({}) | Momen: {}".format(h["hari"], h["tanggal_tampil"], h["tanggal"], momen))


def main():
    ap = argparse.ArgumentParser(description="Kerangka tanggal minggu untuk paket konten mingguan")
    ap.add_argument("--mulai", help="Tanggal Senin awal minggu (YYYY-MM-DD). Harus jatuh pada hari Senin.")
    ap.add_argument("--hari-ini", help="Tanggal acuan 'hari ini' (YYYY-MM-DD). Default: tanggal sistem. "
                                        "Dipakai untuk menghitung 'Senin minggu depan' bila --mulai kosong.")
    ap.add_argument("--gajian-tanggal", default="25,1",
                     help="Daftar tanggal gajian dipisah koma (default '25,1' = gajian tgl 25 & 1)")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    args = ap.parse_args()

    try:
        tanggal_gajian = {int(x) for x in args.gajian_tanggal.split(",") if x.strip()}
    except ValueError:
        galat("--gajian-tanggal harus daftar angka dipisah koma, mis. '25,1'")
    if any(not (1 <= g <= 31) for g in tanggal_gajian):
        galat("--gajian-tanggal harus antara 1 dan 31")

    if args.mulai:
        senin = parse_tanggal(args.mulai, "--mulai")
        if senin.weekday() != 0:
            galat("--mulai ({}) bukan hari Senin (jatuh hari {}). Pakai tanggal Senin, "
                  "atau kosongkan --mulai untuk otomatis pakai Senin minggu depan.".format(
                      args.mulai, HARI[senin.weekday()]))
    else:
        hari_ini = parse_tanggal(args.hari_ini, "--hari-ini") if args.hari_ini else date.today()
        senin = senin_berikutnya(hari_ini)

    data = bangun_minggu(senin, tanggal_gajian)
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        cetak_text(data)


if __name__ == "__main__":
    main()
